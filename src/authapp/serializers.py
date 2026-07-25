from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Un solo grupo
        group = user.groups.first()
        token['group'] = group.name if group else None

        # Permisos efectivos (incluye los del grupo)
        token['permissions'] = list(user.get_all_permissions())

        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        doctor = getattr(user, "doctor_profile", None)
        token["doctor_id"] = doctor.id if doctor else None
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