from django.contrib.auth.models import User
from django.utils import timezone
from Calendar.models import *
from .models import *
from .email import EmailThread
from .console import print_status
from django.core.mail import send_mail
from .console import print_status
from .settings import EMAIL_HOST_USER, DEBUG


def initialize_database():
    print_status('STATUS',str('Initializing test objects'))
    try:
        try:
            patient_user = User.objects.create_user(username='spidey', email='username@example.com', first_name="Peter",last_name="Parker", password='qwertyuiop')
            print_status('GOOD',str('Patient user created.'))
            patient_user.save()
        except Exception as error:
            print_status('FAIL',str('Patient user initialization failed! Attempting to grab existing from DB'))
            patient_user = User.objects.get(username='spidey')

        try:
            nurse_user = User.objects.create_user(username='mj', email='username@example.com', first_name="Mary",last_name="Jane", password='qwertyuiop')
            print_status('GOOD',str('Nurse user created.'))
            nurse_user.save()
        except Exception as error:
            print_status('FAIL',str('Nurse user initialization failed!'))
            nurse_user = User.objects.get(username='mj')

        try:
            doctor_user = User.objects.create_user(username='dococ', email='username@example.com', first_name="Otto",last_name="Octavius", password='qwertyuiop')
            print_status('GOOD',str('Doctor user created.'))
            doctor_user.save()
        except Exception as error:
            doctor_user = User.objects.get(username='dococ')
            print_status('FAIL',str('Doctor user initialization failed!'))

        try:
            test_hospital = Hospital.hospitals.create(name="Test Hospital",address="123 Test Street")
            print_status('GOOD',str('Hospital object created and linked.'))
            test_hospital.save()
        except Exception as error:
            print_status('FAIL',str('Hospital object initialization failed!'))
            raise error

        try:
            test_doctor = Doctor.doctors.create(user=doctor_user,phone_number='+1234568900')
            test_doctor.hospital.add(test_hospital)
            print_status('GOOD',str('Hospital object added to doctor.'))
            test_doctor.save()
            print_status('GOOD',str('Doctor object created and saved to database.'))
        except Exception as error:
            print_status('FAIL',str('Doctor object initialization failed!'))
            raise error

        try:
            test_nurse = Nurse.nurses.create(user=nurse_user,phone_number='+12345678900',hospital=test_hospital)
            test_nurse.save()
            print_status('GOOD',str('Nurse object created and linked.'))
        except Exception as error:
            print_status('FAIL',str('Nurse object initialization failed!'))
            raise error

        try:
            test_patient = Patient.patients.create(user=patient_user,phone_number='+12345678900',height=100,weight=100,doctor=test_doctor, hospital=test_hospital)
            test_patient.save()
            print_status('GOOD',str('Patient object created and linked.'))
        except Exception as error:
            print_status('FAIL',str('Patient object initialization failed!'))
            raise error

        try:
            test_appointment = CalendarEvent.appointments.create(title='test_appointment',start=timezone.now(),end=timezone.now(), patient=test_patient,doctor=test_doctor,hospital=test_hospital)
            test_appointment.save()
            print_status('GOOD',str('Appointment object created, linked, and saved.'))
        except Exception as error:
            print_status('FAIL',str('Appointment object initialization failed!'))
            raise error

    except Exception as error:
        print_status('DATA',str(error))
        raise error



def email_test():
    try:
        print_status('STATUS',str('Please input an email address to act as a recipient for testing'))
        TEST_EMAIL = input('Email: ')
    except EOFError as error:
        print_status('STATUS',str("""Meh, well you're probably in a docker container so we'll forgive you <3"""))
        TEST_EMAIL = ''
    patient = User.objects.get(username='spidey').patient
    doctor = User.objects.get(username='dococ').doctor
    patient.user.email = TEST_EMAIL
    patient.user.save()
    doctor.user.email = TEST_EMAIL
    doctor.user.save()
    appointment = CalendarEvent.appointments.get(title='test_appointment')
    print_status('STAT',str('Sending test email, please check your inbox.'))
    try:
        subject = 'TEST EMAIL PLEASE IGNORE'.format(doctor.user.last_name)
        message = """Hi {}! We're letting you know that your appointment with Doctor {} has been confirmed. Here are the details: \n
The appointment '{}' is scheduled for {}, at your hospital, {}. If you would like to reschedule, please contact your doctor, at {}. Do NOT reply to this email. Thank you, and have a good day!
""".format(patient.user.first_name, doctor.user.last_name, appointment.title, appointment.start, patient.hospital, doctor.user.email)
        EmailThread(subject=subject, message=message, recipient_list=[str(patient.user.email),str(doctor.user.email)]).start()
        print_status('GOOD',str("""Appointment confirmation email to Patient '{} {}' and Doctor '{} {}' about appointment '{}' sent!""".format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name,appointment.title)))
    except Exception as error:
        print_status('WARN',str('Appointment confirmation email to Patient {} {} and Doctor {} {} failed! This is likely because your SMTP settings are incorrect, the email entered as a test recipient was incorrect, of you are using Docker and Evan did not fix the container. If it is the first problem, email functionality will not work without proper settings set in HealthNet/settings.py'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
        print(error)

def delete_test_objects():
    print_status('STATUS',str('Cleanup of database artifacts starting!'))
    appointments = User.objects.get(username='dococ').doctor.calendarevent_set.all()
    hospitals = User.objects.get(username='dococ').doctor.hospital.all()
    for appointment in appointments:
        print_status('DATA',str("""Deleting Appointment ID '{}'""").format(appointment.appointment_id))
        appointment.delete()

    for hospital in hospitals:
        print_status('DATA',str("""Deleting hospital '{}'""").format(hospital.name))
        hospital.delete()

    User.objects.get(username='spidey').delete()
    print_status('GOOD',str('Patient user deleted'))
    User.objects.get(username='mj').delete()
    print_status('GOOD',str('Nurse user deleted'))
    User.objects.get(username='dococ').delete()
    print_status('GOOD',str('Doctor user deleted'))

def settings_warn():
    if(DEBUG == True):
        print_status('STATUS','Debug enviornment currently enabled.')
    if(EMAIL_HOST_USER == 'myhealthnoreply@gmail.com'):
        print_status('HARDWARN','Your EMAIL_HOST_USER enviornment variable in settings.py has NOT been changed from the default. It is HIGHLY reccomended that you change this variable before running this system in a production enviornment')
