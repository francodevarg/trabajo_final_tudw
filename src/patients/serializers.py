from rest_framework import serializers

from patients.models import Patient


class PatientListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Patient
        fields = (
            "id",
            "first_name",
            "last_name",
            "dni",
            "date_of_birth",
            "sex",
            "email",
        )