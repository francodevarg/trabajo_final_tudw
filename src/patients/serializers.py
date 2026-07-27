from rest_framework import serializers

from patients.models import Patient, PatientUser
from evolutions.models import Evolution


class PatientUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = PatientUser
        fields = ("id", "user", "email", "full_name", "is_primary", "role")

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.email


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("first_name", "last_name", "dni", "date_of_birth", "sex")


class PatientListSerializer(serializers.ModelSerializer):
    users = PatientUserSerializer(source="user_links", many=True, read_only=True)

    class Meta:
        model = Patient
        fields = (
            "id",
            "first_name",
            "last_name",
            "dni",
            "date_of_birth",
            "sex",
            "users",
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
            "notes",
        )
