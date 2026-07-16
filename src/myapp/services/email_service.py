from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailService:
    """
    Servicio limpio y estándar para envío de correos.
    Sin adjuntos que activen el clip de descarga en Gmail.
    """

    @classmethod
    def send_otp_email(cls, email, otp, expiration_minutes):
        subject = 'Código de Acceso - Medicare'
        template_name = 'emails/otp.html'    
        # Enviamos las variables exactas que usará el HTML
        context = {
            'otp': otp,
            'expiration_minutes': expiration_minutes,
            'year': timezone.now().year,
        }

        # 1. Renderizar el HTML de la plantilla
        html_content = render_to_string(template_name, context)

        # 2. Crear el correo alternativo plano y el HTML
        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Tu código de acceso a Medicare es: {otp}",
            from_email=None,
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")

        # 3. Enviar
        msg.send(fail_silently=False)
    
    @classmethod
    def send_appointment_confirmation_email(cls, appointment):
        subject = "Turno confirmado - Medicare"
        template_name = "email/appointment_confirmation.html" 
        
        context = {
            "doctor": appointment.doctor.user.first_name + " " + appointment.doctor.user.last_name,
            "date": appointment.date,
            "time": appointment.time,
            "year": timezone.now().year,
            "patient": appointment.patient.first_name,
            "specialty": appointment.doctor.specialty.name,
        }

        html_content = render_to_string(template_name, context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Turno Reservado - Medicare",
            from_email=None,
            to=[appointment.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    @classmethod
    def send_doctor_welcome_email(cls, doctor):
        subject = "Bienvenido a Medicare - MediCare"
        template_name = "email/doctor_welcome.html"

        user = doctor.user
        doctor_name = user.first_name + " " + user.last_name

        context = {
            "doctor_name": doctor_name,
            "specialty": doctor.specialty.name,
            "year": timezone.now().year,
        }

        html_content = render_to_string(template_name, context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Bienvenido a Medicare - MediCare",
            from_email=None,
            to=[doctor.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
