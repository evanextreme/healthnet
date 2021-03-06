from django.contrib import auth
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from django.template import loader, Context, RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from io import BytesIO
from itertools import chain
from reportlab.pdfgen import canvas
from weasyprint import HTML
from Calendar.forms import CalendarEventForm, UpdateCalendarEventForm
from Calendar.models import CalendarEvent, Attachment
from Calendar.util import events_to_json, calendar_options
from EventLog.models import log
from HealthNet.email import *
from HealthNet.forms import *
from HealthNet.models import *

#main index functions
@csrf_exempt
def home(request):
    user = request.user
    permissions = get_permissions(user)
    event_url = 'all_events/'
    opentap = ''
    prescriptions = ''
    patients = ''
    unconfirmed = 0
    appointments = ''
    appointment = ''
    confirmed = False
    released = False
    hospitalnumber = ''
    attachmentnumber = ''
    notification = ''
    error = ''

    #if user logs in first time, the help documentation will show up.
    if (permissions == 'patient' and user.patient.new_user) or (permissions == 'nurse' and user.nurse.new_user) or (permissions == 'doctor' and user.doctor.new_user):
        opentap = 'open'
    
    if permissions == 'patient':
        prescriptions = user.patient.prescription_set.all()
        appointments = user.patient.calendarevent_set.all()
        user.patient.new_user = False
        user.patient.save()
    elif permissions == 'nurse':
        patients = get_nurse_patients(user.nurse)
        appointments = user.nurse.hospital.calendarevent_set.all()
        user.nurse.new_user = False
        user.nurse.save()

    elif permissions == 'doctor':
        unconfirmed = confirmed_appointments(user)
        appointments = user.doctor.calendarevent_set.all()
        patients = user.doctor.patient_set.all()
        hospitalnumber = user.doctor.hospital.all().count()
        user.doctor.new_user = False
        user.doctor.save()
    
    #if user is admin, redirect to admin dashboard
    elif permissions == 'admin':
        return HttpResponseRedirect('/admin')

    variables = RequestContext(request, {'user':user,'opentap':opentap,'calendar_config_options':calendar_options(event_url, OPTIONS),'permissions':permissions,'prescriptions':prescriptions,'patients':patients,'unconfirmed':unconfirmed,'hospitalnumber':hospitalnumber,'attachmentnumber':attachmentnumber,'appointments':appointments,'appointment':appointment,'notification':notification,'error':error})

    #if any action takes
    if request.method == 'POST':
        appointment = CalendarEvent()
        #if has an appointment id, act as "update appointment"
        if 'appointmentId' in request.POST:
            post_id = request.POST['appointmentId']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            attachments = appointment.attachment_set.all()
            attachmentnumber= appointment.attachment_set.all().count()
            cal_form = UpdateCalendarEventForm(instance=appointment)
            if appointment.confirmed == False:
                variables['confirmed'] = 'False'
            else:
                variables['confirmed'] = 'True'
            if appointment.released == False:
                variables['released'] = 'False'
            else:
                variables['released'] = 'True'
            if permissions == 'doctor':
                cal_form.fields['doctor'].widget = forms.HiddenInput()
                cal_form.fields['hospital'].queryset = user.doctor.hospital.all()
                if appointment.confirmed ==False:
                    cal_form.fields['attachments'].widget = forms.HiddenInput()
            elif permissions == 'nurse':
                cal_form.fields['doctor'].widget = forms.HiddenInput()
                cal_form.fields['type'].widget = forms.HiddenInput()
                cal_form.fields['attachments'].widget = forms.HiddenInput()
            elif permissions == 'patient':
                cal_form.fields['doctor'].widget = forms.HiddenInput()
                cal_form.fields['type'].widget = forms.HiddenInput()
                cal_form.fields['attachments'].widget = forms.HiddenInput()
            cal_form.fields['patient'].widget = forms.HiddenInput()
            if permissions != 'doctor' or hospitalnumber == 1:
                cal_form.fields['hospital'].widget = forms.HiddenInput()
            if permissions == 'patient' and appointment.confirmed:
                cal_form.fields['title'].widget.attrs['disabled'] = True
                cal_form.fields['start'].widget.attrs['disabled'] = True
                cal_form.fields['end'].widget.attrs['disabled'] = True
                cal_form.fields['all_day'].widget.attrs['disabled'] = True
            cal_form.fields['appointment_id'].widget = forms.HiddenInput()
            variables['appointment'] = appointment
            variables['attachments'] = attachments
            variables['attachmentnumber'] = attachmentnumber
            variables['cal_form'] = cal_form
            return render_to_response('appointments/update.html', variables)
        #if click "create", act as "create appointment"
        elif 'Create' in request.POST:
            if permissions == 'nurse':
                post_id = request.POST['patient']
                patient = Patient.patients.get(patient_id=post_id)
                doctor_id = patient.doctor.doctor_id
                request.POST['doctor'] = doctor_id

            cal_form = CalendarEventForm(request.POST, request.FILES)

            if permissions == 'doctor':
                cal_form.doctor = user.doctor


            elif permissions == 'patient':
                cal_form.patient = user.patient
                cal_form.doctor = user.patient.doctor
                cal_form.hospital = user.patient.hospital

            if cal_form.is_valid():
                appointment = cal_form.save(commit=False)
                if permissions == 'doctor' or permissions == 'nurse':
                    appointment.confirmed = True
                    appointment.color = '#00b0ff'
                    appointment_confirmation_email(appointment.patient,appointment.doctor,appointment)
                appointment.save()
                for each in cal_form.cleaned_data['attachments']:
                    attachment = Attachment.objects.create(file=each,appointment=appointment)
                    attachment.save()
                event=log(user=user,action="new_appt",notes={})
                event.save()
                if permissions == 'patient':
                    variables['notification'] = str('Please wait your doctor to confirm.')
                return render_to_response('index.html', variables)
            else:
                if permissions == 'doctor':
                    cal_form.fields['doctor'].widget = forms.HiddenInput()
                elif permissions == 'nurse':
                    cal_form.fields['doctor'].widget = forms.HiddenInput()
                    cal_form.fields['type'].widget = forms.HiddenInput()
                    cal_form.fields['attachments'].widget = forms.HiddenInput()
                elif permissions == 'patient':
                    cal_form.fields['patient'].widget = forms.HiddenInput()
                    cal_form.fields['doctor'].widget = forms.HiddenInput()
                    cal_form.fields['type'].widget = forms.HiddenInput()
                    cal_form.fields['attachments'].widget = forms.HiddenInput()
                if permissions != 'doctor' or hospitalnumber == 1:
                    cal_form.fields['hospital'].widget = forms.HiddenInput()

                variables['cal_form'] = cal_form
                variables['error'] = 'new_appointment'
                return render_to_response("index.html",variables)
        
        #if click "update", act as "update appointment"
        elif 'Update' in request.POST:
            post_id = request.POST['appointment_id']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            cal_form = UpdateCalendarEventForm(request.POST, request.FILES, instance=appointment)
            print(str(request.FILES))
            if cal_form.is_valid():
                appointment = cal_form.save()
                if permissions == 'doctor' and appointment.confirmed == False:
                    appointment.confirmed = True
                    appointment.color = '#00b0ff'
                    appointment_confirmation_email(appointment.patient,appointment.doctor,appointment)
                    variables['unconfirmed'] = confirmed_appointments(user)
                    variables['appointments'] = user.doctor.calendarevent_set.all()
                for each in cal_form.cleaned_data['attachments']:
                    print('HIT HIT')
                    attachment = Attachment.objects.create(file=each,appointment=appointment)
                    attachment.save()
                appointment.save()
                if permissions == 'doctor':
                    unconfirmed = confirmed_appointments(user)
                event=log(user=user,action="update_apt",notes={})
                event.save()
                variables['notification'] = str('Appointment successfully updated')
                return render_to_response('index.html', variables)
            else:
                if permissions == 'doctor':
                    cal_form.fields['doctor'].widget = forms.HiddenInput()
                elif permissions == 'nurse':
                    cal_form.fields['doctor'].widget = forms.HiddenInput()
                    cal_form.fields['hospital'].widget = forms.HiddenInput()
                    cal_form.fields['type'].widget = forms.HiddenInput()
                    cal_form.fields['attachments'].widget = forms.HiddenInput()
                elif permissions == 'patient':
                    cal_form.fields['patient'].widget = forms.HiddenInput()
                    cal_form.fields['doctor'].widget = forms.HiddenInput()
                    cal_form.fields['hospital'].widget = forms.HiddenInput()
                    cal_form.fields['type'].widget = forms.HiddenInput()
                    cal_form.fields['attachments'].widget = forms.HiddenInput()

                variables['cal_form'] = cal_form
                variables['error'] = 'update_appointment'
                return render_to_response("index.html",variables)
        
        #if click "delete", act as "delete appointment"
        elif 'Delete' in request.POST:
            post_id = request.POST['appointment_id']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            appointment_deletion_email(appointment.patient, appointment.doctor, appointment)
            appointment.delete()
            event=log(user=user,action="deleted_apt",notes={})
            event.save()
            variables['notification'] = str('Appointment successfully deleted, email sent')
            return render_to_response('index.html', variables)

        #if click "release", act as "release attachment"
        elif 'Release' in request.POST:
            post_id = request.POST['appointment_id']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            appointment.released = True
            appointment.save()
            results_released_email(appointment.patient, appointment.doctor, appointment)
            event=log(user=user,action="released_attachments",notes={})
            event.save()
            variables['notification'] = str('Appointment successfully released, email sent')
            return render_to_response('index.html', variables)

        #if click "create prescription", act as "create prescription"
        elif 'create_prescription' in request.POST:
            form = PrescriptionForm(request.POST)
            if form.is_valid():
                prescription = form.save()
                event=log(user=user,action="new_prescription",notes={})
                if user.doctor:
                    patients = user.doctor.patient_set.all()
                elif user.nurse:
                    patients = user.nurse.patient_set.all()
                prescription_created_email(prescription.patient,user.doctor,prescription)
                variables['notification'] = str('Prescription successfully created, email sent')
                return render_to_response('index.html', variables)
            else:
                variables['cal_form'] = form
                variables['error'] = 'create_prescription'
                return render_to_response("index.html",variables)

        #if click "admit", act as "admit patient to hospital"
        elif 'admit_patient' in request.POST:
            post_id = request.POST['admit_patient']
            patient = Patient.patients.get(patient_id=post_id)
            patient.admitted = True
            patient.save()
            event=log(user=user,action="admit_patient",notes={"patient":str(patient.user.first_name + " " + patient.user.last_name)})
            event.save()
            variables['notification'] = str('{} {} successfully admitted').format(patient.user.first_name,patient.user.last_name)
            return render_to_response('index.html',variables)

        #if click "discharge", act as "discharge patient from hospital"
        elif 'discharge_patient' in request.POST:
            post_id = request.POST['discharge_patient']
            patient = Patient.patients.get(patient_id=post_id)
            patient.admitted = False
            patient.save()
            event=log(user=user,action="admit_patient",notes={"patient":str(patient.user.first_name + " " + patient.user.last_name)})
            event.save()
            variables['notification'] = str('{} {} successfully discharged').format(patient.user.first_name,patient.user.last_name)

            return render_to_response('index.html',variables)
        
        #if click "update patient", act as "update patient's medical information"
        elif 'update_patient' in request.POST:

            post_id = request.POST['patient_id']
            patient = Patient.patients.get(patient_id=post_id)
            patient.save()
            event=log(user=user,action="update_patient",notes={"patient":str(patient.user.first_name + " " + patient.user.last_name)})
            event.save()
            variables['notification'] = str('{} {} successfully updated').format(patient.user.first_name,patient.user.last_name)

            return render_to_response('index.html',variables)

        #if click "edit prescription", act as "edit patient's prescription"
        elif 'update_prescription' in request.POST:
            post_id = request.POST['update_prescription']
            prescription = Prescription.prescriptions.get(prescription_id = post_id)
            prescriptionform = PrescriptionForm(request.POST, instance = prescription)
            if prescriptionform.is_valid():
                prescriptionform.save()
                event = log(user=user, action = "employee_edit_prescription",notes={})
                event.save()
                variables['notification'] = str('Prescription successfully updated')
                return render_to_response('index.html',variables)
            else:
                variables['cal_form'] = prescriptionform
                variables['error'] = 'update_prescription'
                return render_to_response("index.html",variables)

        #if click "refill", act as "the number of remaining - 1"
        elif 'refill_prescription' in request.POST:
            post_id = request.POST['refill_prescription']
            prescription = Prescription.prescriptions.get(prescription_id = post_id)
            prescription.refill()
            prescription.save()
            event = log(user=user, action = "patient_refill_prescription",notes={})
            event.save()
            return render_to_response('index.html', variables)

        #if click "delete prescription", act as "delete prescription"
        elif 'remove_prescription' in request.POST:
            post_id = request.POST['remove_prescription']
            prescription = Prescription.prescriptions.get(prescription_id = post_id)
            prescription.delete()
            event = log(user=user, action = "patient_remove_prescription",notes={})
            event.save()
            return render_to_response('index.html', variables)

    else:
        variables['cal_form'] = CalendarEventForm()
        return render_to_response('index.html',variables)

#for doctor to confirm the appointment
def confirmed_appointments(user):
    appointments = user.doctor.calendarevent_set.all()
    unconfirmed = 0
    for appt in appointments:
        if appt.confirmed == False:
            unconfirmed += 1
    return unconfirmed

#logout function
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

#for admit to register doctors and nurse
@csrf_exempt
def doc_register_page(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        patientform = PatientForm(request.POST, request.FILES)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save(commit=False)
            user.set_password(user.password)
            user.save()

            patient = patientform.save(commit=False)

            patient.user = user
            patient.save()

            event = log(user=patient.user, action="employee_registered",notes={})
            event.save()
            variables=RequestContext(request,{'userform':userform, 'docform':docform})
            return render_to_response("admin/register.html",variables)
    user = request.user
    permissions = get_permissions(user)
    userform=UserForm()
    docform=DoctorForm()
    variables=RequestContext(request,{'userform':userform, 'docform':docform,'permissions':permissions})
    return render_to_response("admin/register.html",variables)

#for patient registration
@csrf_exempt
def register_page(request):

    if request.method == 'POST':
        userform = UserForm(request.POST)
        patientform = PatientForm(request.POST, request.FILES)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save(commit=False)
            user.set_password(user.password)
            user.username = user.username.lower()
            user.first_name = user.first_name.title()
            user.last_name = user.last_name.title()
            user.save()

            patient = patientform.save(commit=False)
            patient.user = user
            patient.save()

            event = log(user=patient.user, action="user_registered",notes={})
            event.save()
            return render_to_response("registration/register_confirmed.html")
        else:
            variables=RequestContext(request,{'userform':userform, 'patientform':patientform})
            return render_to_response("registration/register.html",variables)

    else:
        userform=UserForm()
        patientform=PatientForm()
        patientform.fields['hospital'].label = "Preferred Hospital"
        variables=RequestContext(request,{'userform':userform, 'patientform':patientform})
        return render_to_response("registration/register.html",variables)

#for user to update his/her personal profile
@csrf_exempt
def update_profile(request):
    user = request.user
    permissions = get_permissions(user)
    if request.method == 'POST':
        updateform = UpdateUserForm(request.POST, instance = user)
        p_updateform = UpdatePatientForm(request.POST, instance = user.patient)
        if updateform.is_valid() and p_updateform.is_valid():
            p_updateform.save()
            updateform.save()
            user.first_name = user.first_name.title()
            user.last_name = user.last_name.title()
            user.save()
            event=log(user=user,action="user_updateprofile",notes={})
            event.save()
            return HttpResponseRedirect('/')
    else:
        updateform = UpdateUserForm(initial={
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,})
        p_updateform = UpdatePatientForm(initial={
            'height':user.patient.height,
            'weight':user.patient.weight,
            'phone_number':user.patient.phone_number,})
    variables = RequestContext(request, {'user':user,'update_form':updateform, 'p_updateform':p_updateform,'permissions':permissions})
    return render_to_response('account/profile.html', variables)

#for doctor to update patient's medical information
@csrf_exempt
def update_patient(request):
    user = request.user
    permissions = get_permissions(user)
    if request.method == 'POST':
        post_id = request.POST['patient_id']
        patient = Patient.patients.get(patient_id=post_id)
        patientform = EmployeeUpdatePatientForm(instance = patient)
        return render_to_response('patients/update.html', {'user':user,'patientform':patientform,'permissions':permissions},RequestContext(request))

#for doctor and nurse to view patient's prescriptions
@csrf_exempt
def get_prescriptions(request):
    user = request.user
    permissions = get_permissions(user)
    if request.method == 'POST':
        post_id = request.POST['get_patient_prescriptions']
        if not type(post_id) is int:
            post_id = post_id[0]
        patient = Patient.patients.get(patient_id=post_id)
        prescriptions = patient.prescription_set.all()
        return render_to_response('prescriptions/index.html', {'user':user,'patient':patient,'prescriptions':prescriptions,'permissions':permissions},RequestContext(request))

#for doctor to update patient's perscriptions
@csrf_exempt
def update_prescription(request):
    user = request.user
    permissions = get_permissions(user)
    post_id = request.POST['update_prescription']
    prescription = Prescription.prescriptions.get(prescription_id = post_id)
    prescriptionform = PrescriptionForm(instance = prescription)
    return render_to_response('prescriptions/update.html', {'user':user, 'prescription':prescription, 'prescriptionform':prescriptionform, 'permissions':permissions}, RequestContext(request))

#for doctor to refill patient's perscription
@csrf_exempt
def edit_prescription(request):
    user = request.user
    permissions = get_permissions(user)
    if request.method == 'POST' and 'refill' in request.POST:
        if request.POST.get("refill"):
            post_id = request.POST['prescription_id']
            prescription = Prescription.prescriptions.get(prescription_id = post_id)
            prescription.refill()
            prescription.save()
            event=log(user=user,action="refill_prescription",notes={})
            event.save()
        elif request.POST.get("remove"):
            post_id = request.POST['prescription_id']
            prescription = Prescription.prescriptions.get(prescription_id = post_id)
            prescription.delete()
            event=log(user=user,action="delete_prescription",notes={})
            event.save()
            prescriptions = user.patient.prescription_set.all()
            return render_to_response('account/prescriptions.html', {'user':user, 'permissions':permissions,'prescriptions':prescriptions}, RequestContext(request))
        return render_to_response('account/edit_prescription.html', {'user':user, 'prescriptionform':form,'prescription':prescription, 'permissions':permissions}, RequestContext(request))

#for doctor to create new prescription
@csrf_exempt
def new_prescription(request):
    user = request.user
    permissions = get_permissions(user)
    form = PrescriptionForm()
    if permissions == 'doctor':
        form.fields['patient'].queryset = user.doctor.patient_set.all()

    return render_to_response('prescriptions/new.html', {'user':user, 'prescriptionform':form, 'permissions':permissions}, RequestContext(request))

#for doctor and nurse transfer patient into another hospital
@csrf_exempt
def change_hospital(request):
    user = request.user
    if request.method == 'POST':
        hospital_change_form = DoctorForm(request.POST, instance = user)
        if hospital_change_form.is_valid():
            hospital_change_form.save()
            event=log(user=user,action="change_doctor_hosptial",notes={})
            event.save()
            return HttpResponseRedirect('/')
    hospital_change_form = DoctorForm(initial={'hospital':user.doctor.hospital})
    variables = RequestContext(request, {'user':user,'hospital_change_form':hospital_change_form})
    return render_to_response('account/change_hospital.html', variables)

#for user to change password
@csrf_exempt
def change_password(request):
    prescriptions = ''
    patients = ''
    unconfirmed = 0
    appointments = ''
    user = request.user
    permissions = get_permissions(user)

    if request.method == 'POST':
        passform = PasswordChangeForm(user, request.POST)
        if passform.is_valid():
            user = passform.save()
            auth.update_session_auth_hash(request, user)
            event=log(user=user,action="user_updatepassword",notes={})
            event.save()
            return HttpResponseRedirect('/')
        else:
            variables = RequestContext(request, {'user':user,'password_form':passform,'permissions':permissions,'appointments':appointments,'unconfirmed':unconfirmed})
            return render_to_response('account/password.html', variables)

    else:

        passform = PasswordChangeForm(user)
        variables = RequestContext(request, {'user':user,'password_form':passform,'permissions':permissions,'appointments':appointments,'unconfirmed':unconfirmed})
        return render_to_response('account/password.html', variables)

#check how many unconfirmed appointments for the doctor and show the number in the dashboard
def account(request):
    user = request.user
    permissions = get_permissions(user)
    unconfirmed = 0
    if permissions == 'doctor':
        appointments = user.doctor.calendarevent_set.all()
        for appt in appointments:
            if appt.confirmed == False:
                unconfirmed += 1
    variables = RequestContext(request, {'user':user,'permissions':permissions,'unconfirmed':unconfirmed})
    return render_to_response('account/index.html', variables)

#for patient view prescriptions
@csrf_exempt
def prescriptions(request):
    user = request.user
    permissions = get_permissions(user)
    prescriptions = user.patient.prescription_set.all()
    variables = RequestContext(request, {'user':user,'permissions':permissions, 'prescriptions':prescriptions})
    return render_to_response('account/prescriptions.html', variables)

#for doctor and nurse view their patients
def patients(request):
    user = request.user
    permissions = get_permissions(user)
    if permissions == 'doctor':
        patients = user.doctor.patient_set.all()
        variables = RequestContext(request, {'user':user,'patients':patients,'permissions':permissions})
        return render_to_response('patients/index.html',variables)
    elif permissions == 'nurse':
        patients = user.nurse.hospital.patient_set.all()
        variables = RequestContext(request, {'user':user,'patients':patients,'permissions':permissions})
        return render_to_response('patients/index.html',variables)

#for user to create new appointment
@csrf_exempt
def new_appt(request):
    user = request.user
    permissions = get_permissions(user)
    hospitalnumber = ''
    justone = ''
    if request.method != 'POST':
        if permissions == 'doctor':
            hospitalnumber=user.doctor.hospital.all().count()
            if hospitalnumber == 1:
                for h in user.doctor.hospital.all():
                    justone = h
                cal_form = CalendarEventForm(initial={'doctor': user.doctor,'hospital':justone})
                cal_form.fields['hospital'].widget = forms.HiddenInput()
            else:
                cal_form = CalendarEventForm(initial={'doctor': user.doctor})
                cal_form.fields['hospital'].queryset = user.doctor.hospital.all()
            cal_form.fields['doctor'].widget = forms.HiddenInput()
            cal_form.fields['patient'].queryset = user.doctor.patient_set.all()
        elif permissions == 'nurse':
            cal_form = CalendarEventForm(initial={'hospital': user.nurse.hospital})
            cal_form.fields['doctor'].widget = forms.HiddenInput()
            cal_form.fields['hospital'].widget = forms.HiddenInput()
            cal_form.fields['type'].widget = forms.HiddenInput()
            cal_form.fields['attachments'].widget = forms.HiddenInput()
            cal_form.fields['patient'].queryset = get_nurse_patients(user.nurse)
        elif permissions == 'patient':
            cal_form = CalendarEventForm(initial={'patient': user.patient,
                                                  'doctor': user.patient.doctor,
                                                  'hospital': user.patient.hospital})
            cal_form.fields['patient'].widget = forms.HiddenInput()
            cal_form.fields['doctor'].widget = forms.HiddenInput()
            cal_form.fields['hospital'].widget = forms.HiddenInput()
            cal_form.fields['type'].widget = forms.HiddenInput()
            cal_form.fields['attachments'].widget = forms.HiddenInput()
        else:
            cal_form = CalendarEventForm()
        variables=RequestContext(request,{'user':user,'cal_form':cal_form,'hospitalnumber':hospitalnumber,'justone':justone,'permissions':permissions})
        return render_to_response("appointments/new.html",variables)

#for doctor to create new test
def new_test(request):
    user = request.user
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            for each in form.cleaned_data['attachments']:
                Attachment.objects.create(file=each)

#for patient to export his/her information
def export_file(request):
    user = request.user
    permissions = get_permissions(user)
    if permissions == 'patient':
        appointments = user.patient.calendarevent_set.all()
    elif permissions == 'nurse':
        appointments = user.nurse.calendarevent_set.all()
    elif permissions == 'doctor':
        appointments = user.doctor.calendarevent_set.all()
    html_string = render_to_string('export/template.html', {'user': user,'permissions':permissions,'appointments':appointments})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/myHealthExport.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('myHealthExport.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="myHealthExport.pdf"'
        event=log(user=user,action="user_export_file",notes={})
        event.save()
        return response
    return response

#get user's permission
def get_permissions(user):
    if hasattr(user, 'patient'):
        return 'patient'
    elif hasattr(user, 'doctor'):
        return 'doctor'
    elif hasattr(user, 'nurse'):
        return 'nurse'
    elif user.is_superuser:
        return 'admin'
    else:
        return 'none'

#get user's all appointments
def all_events(request):
    user = request.user
    permissions = get_permissions(user)
    if permissions == 'patient':
        appointments = user.patient.calendarevent_set.all()
    elif permissions == 'doctor':
        appointments = user.doctor.calendarevent_set.all()
    elif permissions == 'nurse':
        appointments = user.nurse.hospital.calendarevent_set.all()
    return HttpResponse(events_to_json(appointments), content_type='application/json')

#for doctor and nurse to get the patient card for each of their patients
@csrf_exempt
def get_card(request):
    if 'patientid' in request.POST:
        post_id = request.POST['patientid']
        patient = Patient.patients.get(patient_id=post_id)
        variables = {'user':patient.user}
        return(render_to_response('card/patientplus.html',variables))

#for nurse to get his/her patients from his/her hospital
def get_nurse_patients(nurse):
    doctors = nurse.hospital.doctor_set.all()
    nurse_patients = Patient.patients.none()
    for doctor in doctors:
        nurse_patients = nurse_patients | doctor.patient_set.all()
    return nurse_patients

OPTIONS = """{  timeFormat: "H:mm",

                editable: false,
                handleWindowResize: true,
                defaultView: 'agendaWeek', // Only show week view
                header: {
                    left: 'prev,next today',
                    right: 'month,agendaWeek,agendaDay',
                },
                minTime: '07:30:00', // Start time for the calendar
                maxTime: '22:00:00', // End time for the calendar
                columnFormat: {
                    week: 'ddd M/d' // Only show day of the week names
                },
                displayEventTime: true,
                allDayText: 'Unscheduled',

                eventClick: function(event, jsEvent, view) {
                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                function getCookie(name) {
                                    var cookieValue = null;
                                    if (document.cookie && document.cookie != '') {
                                        var cookies = document.cookie.split(';');
                                        for (var i = 0; i < cookies.length; i++) {
                                            var cookie = jQuery.trim(cookies[i]);
                                            // Does this cookie string begin with the name we want?
                                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                                break;
                                            }
                                        }
                                    }
                                    return cookieValue;
                                }
                                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                                    // Only send the token to relative URLs i.e. locally.
                                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                                }
                            }
                        });

                        $.post('/', event, function(response){
                            $('#apt-div').html(response);
                        });
                        $('#apt-modal').modal('open');

                },
            }"""
