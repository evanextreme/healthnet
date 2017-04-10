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
from Calendar.models import CalendarEvent
from Calendar.util import events_to_json, calendar_options
from Calendar.forms import CalendarEventForm
from django.contrib.auth.forms import PasswordChangeForm

@csrf_exempt
def home(request):
    user = request.user
    event_url = 'all_events/'
    if request.method == 'POST':
        appointment = CalendarEvent()
        if 'appointmentid' in request.POST:
            post_id = request.POST['appointmentid']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            cal_form = CalendarEventForm(instance=appointment)
            cal_form.fields['appointment_id'].widget = forms.HiddenInput()
            cal_form.fields['patient'].widget = forms.HiddenInput()
            variables = RequestContext(request, {'user':user,'cal_form':cal_form,'calendar_config_options':calendar_options(event_url, OPTIONS)})
            return render_to_response('appointments/update.html', variables)
        else:
            post_id = request.POST['appointment_id']
            appointment = CalendarEvent.appointments.get(appointment_id=post_id)
            cal_form = CalendarEventForm(request.POST, instance=appointment)
            if cal_form.is_valid():
                cal_form.save()
                event=log(user=user,action="updated_apt")
                event.save()
                variables = RequestContext(request, {'user':user,'cal_form':cal_form,'calendar_config_options':calendar_options(event_url, OPTIONS)})
                return render_to_response('index.html', variables)
            else:
                print(str(cal_form.errors))

    else:
        cal_form = CalendarEventForm()
        variables = RequestContext(request, {'user':user,'cal_form':cal_form,'calendar_config_options':calendar_options(event_url, OPTIONS)})
        return render_to_response('index.html',variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def doc_register_page(request):
    if request_method == 'POST':
        userform = UserForm(data=request.POST)
        docform = DoctorForm(data=reuqest.POST)
        if userform.is_valid() and docform.is_valid():
            user = userform.save(commit=False)
            user.set_password(user.password)
            user.save()

            doctor = docform.save(commit=False)
            doctor.user = user
            doctor.save()

            event = log(user=patient.user, action="user_registered")
            event.save()

            response = HttpResponse()
            #TODO fix response
            response.write("<h1>Congratulation! You are registered!</h1>")
            response.write("<h2>Please <a href='../login/'>log in</a>.</h2>")

    userform=UserForm()
    docform=DoctorForm()
    variables=RequestContext(request,{'userform':userform, 'docform':docform})
    return render_to_response("registration/register.html",variables)


@csrf_exempt
def register_page(request):

    if request.method == 'POST':
        userform = UserForm(data=request.POST)
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
            response = HttpResponse()
            #TODO fix response
            response.write("<h1>Congratulation! You are registered!</h1>")
            response.write("<h2>Please <a href='../login/'>log in</a>.</h2>")
            return response

    userform=UserForm()
    patientform=PatientForm()
    variables=RequestContext(request,{'userform':userform, 'patientform':patientform})
    return render_to_response("registration/register.html",variables)

@csrf_exempt
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        updateform = UpdateUserForm(request.POST, instance = user)
        p_updateform = UpdatePatientForm(request.POST, instance = user.patient)
        if updateform.is_valid() and p_updateform.is_valid():
            p_updateform.save()
            updateform.save()
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
            'assigned_doctor':user.patient.assigned_doctor,
            'current_hospital_assignment':user.patient.current_hospital_assignment,})
        variables = RequestContext(request, {'user':user,'update_form':updateform, 'p_updateform':p_updateform})
        return render_to_response('account/profile.html', variables)

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
    hospital_change_form = DoctorForm(initial={'current_hospital_assignment':user.doctor.current_hospital_assignment})
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
        variables = RequestContext(request, {'user':user,'password_form':passform})
        return render_to_response('account/password.html', variables)


def account(request):
    user = request.user
    variables = RequestContext(request, {'user':user})
    return render_to_response('account/index.html', variables)

@csrf_exempt
def new_appt(request):
    user = request.user
    if request.method == 'POST':
        cal_form = CalendarEventForm(request.POST)
        if cal_form.is_valid():
            appt = cal_form.save(commit=False)
            appt.patient = user.patient
            appt.save()
            event=log(user=user,action="new_appt")
            event.save()
            return HttpResponseRedirect('/')
    else:
        cal_form = CalendarEventForm()
        variables=RequestContext(request,{'user':user,'cal_form':cal_form})
        return render_to_response("appointments/new.html",variables)

@csrf_protect
def update_appointment(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST['appointmentid']
        appointment = CalendarEvent.appointments.get(appointment_id=post_id)
        cal_form = CalendarEventForm(request.POST, instance=appointment)
        variables = RequestContext(request, {'user':user,'cal_form':cal_form})
        return render_to_response('appointments/update.html', variables)

def all_events(request):
    user = request.user
    if hasattr(user, 'patient'):
        appointments = user.patient.calendarevent_set.all()
    elif hasattr(user, 'doctor'):
        appointments = user.doctor.calendarevent_set.all()
    return HttpResponse(events_to_json(appointments), content_type='application/json')


OPTIONS = """{  timeFormat: "H:mm",
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay',
                },
                allDaySlot: true,
                firstDay: 0,
                weekMode: 'liquid',
                slotMinutes: 15,
                defaultEventMinutes: 30,
                minTime: 0,
                maxTime: 24,
                editable: true,

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
                            alert(response)
                            $('#update-apt-div').html(response);
                        });
                        $('#update-apt-modal').modal('open');

                },
            }"""
