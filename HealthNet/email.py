from django.core.mail import send_mail
from .console import print_status

def appointment_confirmation_email(patient, doctor, appointment):
    try:
        subject = 'Your appointment with Doctor {} has been confirmed!'.format(doctor.user.last_name)
        message = """Hi {}! We're letting you know that your appointment with Doctor {} has been confirmed. Here are the details: \n
                The appointment is scheduled for {}, at your hospital, {}. If you would like to reschedule, please contact your doctor, at {}. Do NOT reply to this email. Thank you, and have a good day!
                """.format(patient.user.first_name, doctor.user.last_name, appointment.start, patient.hospital, doctor.user.email)
        send_mail(
            subject,
            message,
            ['noreply@health.net'],
            [patient.user.email],
            fail_silently=False,
        )
    except Exception as error:
        print_status('FAIL',str('Appointment confirmation email to Patient {} {} and Doctor {} {} failed!'.format(patient.user.first_name,patient.user.last_name,doctor.user.first_name,doctor.user.last_name)))
