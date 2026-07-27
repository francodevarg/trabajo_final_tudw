from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from patients.models import PatientUser

class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        group = user.groups.first()
        token['group'] = group.name if group else None

        token['permissions'] = list(user.get_all_permissions())

        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        doctor = getattr(user, "doctor_profile", None)
        token["doctor_id"] = doctor.id if doctor else None

        primary_link = PatientUser.objects.filter(
            user=user, is_primary=True
        ).select_related("patient").first()
        token["primary_patient_id"] = (
            primary_link.patient_id if primary_link else None
        )

        token["patient_ids"] = list(
            PatientUser.objects.filter(user=user).values_list(
                "patient_id", flat=True
            )
        )

        return token

class RequestPatientAccessSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower().strip()


class VerifyPatientAccessSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate_email(self, value):
        return value.lower().strip()


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower().strip()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate_email(self, value):
        return value.lower().strip()