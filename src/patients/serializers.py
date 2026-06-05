from rest_framework import serializers

from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "dni",
            "sex",
            "date_of_birth",
            "created_at",
            "updated_at",
        ]
