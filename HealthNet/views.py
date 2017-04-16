from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import loader, Context
from django.contrib.auth import logout
from HealthNet.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from eventlog.models import log
from HealthNet.models import *
from django.contrib.auth.models import User
from Calendar.models import CalendarEvent, Attachment
from Calendar.util import events_to_json, calendar_options
from Calendar.forms import CalendarEventForm, UpdateCalendarEventForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from HealthNet.email import appointment_confirmation_email
from io import BytesIO
from reportlab.pdfgen import canvas


@csrf_exempt
def home(request):
    user = request.user
    permissions = get_permissions(user)
    event_url = 'all_events/'
    opentap = ''
    if (permissions == 'patient' and user.patient.new_user) or (permissions == 'nurse' and user.nurse.new_user) or (permissions == 'doctor' and user.doctor.new_user):
        opentap = 'True'
    #If user is admin, redirect to admin dashboard
    if permissions == 'admin':
        return HttpResponseRedirect('/admin')

    if request.method == 'POST':
        appointment = CalendarEvent()
        if 'appointmentId' in request.POST:
            post_id = request.POST['appointmentId']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            attachments = appointment.attachment_set.all()
            cal_form = UpdateCalendarEventForm(instance=appointment)
            print(str(appointment.confirmed))
            confirmed = 'False'
            if appointment.confirmed == False:
                confirmed = 'False'
            else:
                confirmed = 'True'
            if permissions == 'doctor':
                cal_form.fields['doctor'].widget = forms.HiddenInput()
            elif permissions == 'patient':
                cal_form.fields['patient'].widget = forms.HiddenInput()
                cal_form.fields['type'].widget = forms.HiddenInput()
                cal_form.fields['attachments'].widget = forms.HiddenInput()
            if permissions == 'patient' and appointment.confirmed:
                cal_form.fields['title'].widget.attrs['disabled'] = True
                cal_form.fields['start'].widget.attrs['disabled'] = True
                cal_form.fields['end'].widget.attrs['disabled'] = True
                cal_form.fields['all_day'].widget.attrs['disabled'] = True
            cal_form.fields['appointment_id'].widget = forms.HiddenInput()
            variables = RequestContext(request, {'user':user,'cal_form':cal_form,'attachments':attachments,'confirmed':confirmed,'permissions':permissions,'calendar_config_options':calendar_options(event_url, OPTIONS)})
            return render_to_response('appointments/update.html', variables)
        elif 'Create' in request.POST:
            cal_form = CalendarEventForm(request.POST, request.FILES)
            if cal_form.is_valid():
                appointment = cal_form.save(commit=False)
                if permissions == 'doctor' or permissions == 'nurse':
                    appointment.confirmed = True
                    appointment.color = '#00b0ff'
                    #TODO change from confirmation email to creation email
                    appointment_confirmation_email(appointment.patient,appointment.doctor,appointment)
                if get_permissions(user) == 'doctor':
                    appointment.doctor = user.doctor
                elif get_permissions(user) == 'patient':
                    appointment.patient = user.patient
                    appointment.doctor = user.patient.doctor
                    appointment.hospital= user.patient.hospital
                appointment.save()
                for each in cal_form.cleaned_data['attachments']:
                    attachment = Attachment.objects.create(file=each,appointment=appointment)
                    attachment.save()
                event=log(user=user,action="new_appt")
                event.save()
                return HttpResponseRedirect('/')
            else:
                variables = RequestContext(request, {'user':user,'cal_form':cal_form,'calendar_config_options':calendar_options(event_url, OPTIONS),'permissions':permissions})
                return render_to_response("appointments/new.html",variables)
        elif 'Update' in request.POST:
            post_id = request.POST['appointment_id']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            cal_form = UpdateCalendarEventForm(request.POST, request.FILES, instance=appointment)
            if cal_form.is_valid():
                appointment = cal_form.save()
                if permissions == 'doctor' and appointment.confirmed == False:
                    appointment.confirmed = True
                    appointment.color = '#00b0ff'
                    appointment_confirmation_email(appointment.patient,appointment.doctor,appointment)
                for each in cal_form.cleaned_data['attachments']:
                    attachment = Attachment.objects.create(file=each,appointment=appointment)
                    attachment.save()
                appointment.save()
                event=log(user=user,action="update_apt")
                event.save()
                variables = RequestContext(request, {'user':user,'cal_form':cal_form,'calendar_config_options':calendar_options(event_url, OPTIONS),'permissions':permissions})
                return render_to_response('index.html', variables)
            else:
                print(str(cal_form.errors))

        elif 'Delete' in request.POST:
            post_id = request.POST['appointment_id']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            appointment.delete()
            event=log(user=user,action="deleted_apt")
            event.save()
            variables = RequestContext(request, {'user':user,'calendar_config_options':calendar_options(event_url, OPTIONS),'permissions':permissions})
            return render_to_response('index.html', variables)

    else:
        cal_form = CalendarEventForm()
        variables = RequestContext(request, {'user':user,'opentap':opentap,'cal_form':cal_form,'calendar_config_options':calendar_options(event_url, OPTIONS),'permissions':permissions})
        return render_to_response('index.html',variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

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

            event = log(user=patient.user, action="user_registered")
            event.save()
            variables=RequestContext(request,{'userform':userform, 'docform':docform})
            return render_to_response("admin/register.html",variables)
    user = request.user
    permissions = get_permissions(user)
    userform=UserForm()
    docform=DoctorForm()
    variables=RequestContext(request,{'userform':userform, 'docform':docform,'permissions':permissions})
    return render_to_response("admin/register.html",variables)


@csrf_exempt
def register_page(request):

    if request.method == 'POST':
        userform = UserForm(data=request.POST)
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

            event = log(user=patient.user, action="user_registered")
            event.save()
            response = HttpResponse()
            #TODO fix response
            response.write("<h1>Congratulation! You are registered!</h1>")
            response.write("<h2>Please <a href='../login/'>log in</a>.</h2>")
            return response
        else:
            variables=RequestContext(request,{'userform':userform, 'patientform':patientform})
            return render_to_response("registration/register.html",variables)

    else:
        userform=UserForm()
        patientform=PatientForm()
        variables=RequestContext(request,{'userform':userform, 'patientform':patientform})
        return render_to_response("registration/register.html",variables)

@csrf_exempt
def update_profile(request):
    user = request.user
    permissions = get_permissions(user)
    if request.method == 'POST':
        print(str(request.POST))
        updateform = UpdateUserForm(request.POST, instance = user)
        p_updateform = UpdatePatientForm(request.POST, instance = user.patient)
        if updateform.is_valid() and p_updateform.is_valid():
            p_updateform.save()
            updateform.save()
            user.first_name = user.first_name.title()
            user.last_name = user.last_name.title()
            user.save()
            event=log(user=user,action="user_updateprofile")
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
            'assigned_doctor':user.patient.doctor,
            'current_hospital_assignment':user.patient.hospital})
    variables = RequestContext(request, {'user':user,'update_form':updateform, 'p_updateform':p_updateform,'permissions':permissions})
    return render_to_response('account/profile.html', variables)

@csrf_exempt
def employee_update_patient(request):
    user = request.user
    permissions = get_permissions(user)
    if request.method == 'POST' and 'get_patient_id' in request.POST:
        post_id = request.POST['get_patient_id']
        patient = Patient.patients.get(patient_id=post_id)
        patientform = EmployeeUpdatePatientForm(instance = patient)
        if permissions == 'nurse':
            patientform.fields['hospital'].widget = forms.HiddenInput()
    elif request.method == 'POST':
        post_id = request.POST['patient_id']
        patient = Patient.patients.get(patient_id=post_id)
        patientform = EmployeeUpdatePatientForm(request.POST, instance = patient)
        if patientform.is_valid():
            patientform.save()
            event=log(user=user,action="employee_updateprofile")
            event.save()
    return render_to_response('patients/update.html', {'user':user,'patientform':patientform,'permissions':permissions},RequestContext(request))

@csrf_exempt
def edit_prescription(request):
    user = request.user
    permissions = get_permissions(user)
    if request.method == 'POST' and 'refill' in request.POST:
        post_id = request.POST['prescription_id']
        prescription = Prescription.prescriptions.get(prescription_id = post_id)
        prescription.refill()
        prescription.save()
    if request.method == 'POST':
        post_id = request.POST['prescription_id']
        prescription = Prescription.prescriptions.get(prescription_id = post_id)
        form = PrescriptionForm(instance=prescription)
        form.fields['patient'].widget = forms.HiddenInput()
        if permissions != 'doctor' or permissions != 'nurse':
            fields = ['patient', 'drug_name', 'dosage', 'side_effects', 'refills_remaining']
            form.fields['drug_name'].widget = forms.HiddenInput()
            form.fields['dosage'].widget = forms.HiddenInput()
            form.fields['side_effects'].widget = forms.HiddenInput()
            form.fields['refills_remaining'].widget.attrs['readonly'] = True
        return render_to_response('account/edit_prescription.html', {'user':user, 'prescriptionform':form,'prescription':prescription, 'permissions':permissions}, RequestContext(request))



@csrf_exempt
def change_hospital(request):
    user = request.user
    if request.method == 'POST':
        hospital_change_form = DoctorForm(request.POST, instance = user)
        if hospital_change_form.is_valid():
            hospital_change_form.save()
            event=log(user=user,action="doctor_changehosptial")
            event.save()
            return HttpResponseRedirect('/')
    hospital_change_form = DoctorForm(initial={'hospital':user.doctor.hospital})
    variables = RequestContext(request, {'user':user,'hospital_change_form':hospital_change_form})
    return render_to_response('account/change_hospital.html', variables)


@csrf_exempt
def change_password(request):
    user = request.user
    if request.method == 'POST':
        passform = PasswordChangeForm(user, request.POST)
        if passform.is_valid():
            user = passform.save()
            auth.update_session_auth_hash(request, user)
            event=log(user=user,action="user_updatepassword")
            event.save()
            return HttpResponseRedirect('/')
    else:
        passform = PasswordChangeForm(user)
        variables = RequestContext(request, {'user':user,'password_form':passform,'permissions':permissions})
        return render_to_response('account/password.html', variables)


def account(request):
    user = request.user
    permissions = get_permissions(user)
    variables = RequestContext(request, {'user':user,'permissions':permissions})
    return render_to_response('account/index.html', variables)

def prescriptions(request):
    user = request.user
    permissions = get_permissions(user)
    prescriptions = user.patient.prescription_set.all()
    variables = RequestContext(request, {'user':user,'permissions':permissions, 'prescriptions':prescriptions})
    return render_to_response('account/prescriptions.html', variables)


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


@csrf_exempt
def new_appt(request):
    user = request.user
    permissions = get_permissions(user)
    if request.method != 'POST':
        if permissions == 'doctor':
            cal_form = CalendarEventForm(initial={'doctor': user.doctor})
            cal_form.fields['doctor'].widget = forms.HiddenInput()
        elif permissions == 'patient':
            cal_form = CalendarEventForm(initial={'patient': user.patient})
            cal_form.fields['doctor'].widget.attrs['disabled'] = True
            cal_form.fields['hospital'].widget.attrs['disabled'] = True
            cal_form.fields['patient'].widget = forms.HiddenInput()
            cal_form.fields['type'].widget = forms.HiddenInput()
            cal_form.fields['attachments'].widget = forms.HiddenInput()
        else:
            cal_form = CalendarEventForm()
        variables=RequestContext(request,{'user':user,'cal_form':cal_form,'permissions':permissions})
        return render_to_response("appointments/new.html",variables)

def new_test(request):
    user = request.user
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            for each in form.cleaned_data['attachments']:
                Attachment.objects.create(file=each)

def export_file(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, 'Hello world.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

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
        return 'None'

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
                    week: 'ddd' // Only show day of the week names
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
