from django.core.mail import send_mail
from .console import print_status
from .settings import EMAIL_HOST_USER
import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run (self):
        send_mail(
            subject=self.subject,
            message=self.message,
            from_email=EMAIL_HOST_USER,
            recipient_list=self.recipient_list,
            fail_silently=False,
        )


def appointment_confirmation_email(patient, doctor, appointment):
    try:
        subject = 'Your appointment with Doctor {} has been confirmed!'.format(doctor.user.last_name)
        message = """Hi {}! We're letting you know that your appointment with Doctor {} has been confirmed. Here are the details: \n
The appointment '{}' is scheduled for {}, at your hospital, {}. If you would like to reschedule, please contact your doctor, at {}. Do NOT reply to this email. Thank you, and have a good day!
""".format(patient.user.first_name, doctor.user.last_name, appointment.title, appointment.start, patient.hospital, doctor.user.email)
        EmailThread(subject=subject, message=message, recipient_list=[str(patient.user.email),str(doctor.user.email)]).start()
        print_status('GOOD',str('Appointment confirmation email to Patient {} {} and Doctor {} {} sent!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
    except Exception as error:
        print_status('FAIL',str('Appointment confirmation email to Patient {} {} and Doctor {} {} failed!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
        print(error)


def appointment_deletion_email(patient, doctor, appointment):
    try:
        subject = 'Your appointment with Doctor {} has been deleted.'.format(doctor.user.last_name)
        message = """Hi {}! We're letting you know that your appointment with Doctor {} has been deleted. Here are the details of the previous appointment: \n
The appointment '{}' was scheduled for {}, at your hospital, {}. If you would like to reschedule, please contact your doctor, at {}. Do NOT reply to this email. Thank you, and have a good day!
""".format(patient.user.first_name, doctor.user.last_name, appointment.title, appointment.start, patient.hospital, doctor.user.email)
        EmailThread(subject=subject, message=message, recipient_list=[str(patient.user.email),str(doctor.user.email)]).start()
        print_status('GOOD',str('Appointment confirmation email to Patient {} {} and Doctor {} {} sent!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
    except Exception as error:
        print_status('FAIL',str('Appointment deletion email to Patient {} {} and Doctor {} {} failed!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
        print(error)

def results_released_email(patient, doctor, appointment):
    try:
        subject = 'Your results for {} are now available.'.format(appointment.title)
        message = """We're letting you know that results for your appointment/test have been released, and can be viewed online.
The event '{}' took place {}, at your hospital, {}. If you would like to reschedule, please contact your doctor, at {}. Please do NOT reply to this email.
""".format(patient.user.first_name, doctor.user.last_name, appointment.title, appointment.start, patient.hospital, doctor.user.email)
        EmailThread(subject=subject, message=message, recipient_list=[str(patient.user.email),str(doctor.user.email)]).start()
        print_status('GOOD',str('Appointment confirmation email to Patient {} {} and Doctor {} {} sent!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
    except Exception as error:
        print_status('FAIL',str('Appointment deletion email to Patient {} {} and Doctor {} {} failed!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
        print(error)

def prescription_created_email(patient, doctor, prescription):
    try:
        subject = 'A new prescription has been added.'.format(appointment.title)
        message = """Your doctor, Dr. {} {} has given you a new prescription on myHealth. Here are the details.
Prescription Name: {}
Dosage: {}
Instructions: {}
If you have any questions, please contact your doctor, at {}. Please do NOT reply to this email.
""".format(patient.user.first_name, doctor.user.last_name, prescription.drug_name, prescription.dosage, prescription.instructions, doctor.user.email)
        EmailThread(subject=subject, message=message, recipient_list=[str(patient.user.email),str(doctor.user.email)]).start()
        print_status('GOOD',str('Prescription creation email to Patient {} {} and Doctor {} {} sent!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
    except Exception as error:
        print_status('FAIL',str('Prescription creation email to Patient {} {} and Doctor {} {} failed!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
        print(error)
