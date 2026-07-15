import random
from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMessage
from django.utils import timezone
from myapp.services.email_service import EmailService
from authapp.models import OTPCode


class OTPService:

    OTP_EXPIRATION_MINUTES = 5

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @classmethod
    def create_otp_for_user(cls, user):

        otp = cls.generate_otp()

        expires_at = timezone.now() + timedelta(
            minutes=cls.OTP_EXPIRATION_MINUTES
        )

        OTPCode.objects.create(
            user=user,
            code_hash=make_password(otp),
            expires_at=expires_at
        )

        cls.send_otp_email(user.email, otp)

    @staticmethod
    def send_otp_email(email, otp):
      EmailService.send_otp_email(email, otp, OTPService.OTP_EXPIRATION_MINUTES)

    @staticmethod
    def validate_otp(user, code):

        otp_obj = (
            OTPCode.objects
            .filter(
                user=user,
                used=False,
                expires_at__gte=timezone.now()
            )
            .order_by('-created_at')
            .first()
        )

        if not otp_obj:
            return False

        is_valid = check_password(code, otp_obj.code_hash)

        if not is_valid:
            return False

        otp_obj.used = True
        otp_obj.save(update_fields=['used'])

        return True