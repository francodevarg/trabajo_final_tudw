from rest_framework import serializers

from patients.models import Patient
from evolutions.models import Evolution


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



class PatientHistorySerializer(serializers.ModelSerializer):
    appointment = serializers.IntegerField(source="appointment.id")
    date = serializers.DateField(source="appointment.date")
    doctor = serializers.CharField(source="appointment.doctor.user.get_full_name")
    specialty = serializers.CharField(source="appointment.doctor.specialty.name")
    evolution_id = serializers.IntegerField(source="id")

    class Meta:
        model = Evolution
        fields = (
            "appointment",
            "date",
            "doctor",
            "specialty",
            "diagnosis",
            "evolution_id",
            "reason",
            "treatment",
            "notes"
        )