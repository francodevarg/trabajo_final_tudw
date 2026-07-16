from rest_framework import serializers

from .models import Appointment
from doctor.models import Doctor
from patients.models import Patient
from myapp.services.email_service import EmailService


class AppointmentDoctorSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all()
    )


class AppointmentPatientSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    dni = serializers.CharField(max_length=20)
    sex = serializers.ChoiceField(
        choices=Patient.SexChoices.choices
    )
    date_of_birth = serializers.DateField()


class AppointmentDoctorReadSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )

    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )

    specialty = serializers.CharField(
        source="specialty.name",
        read_only=True,
    )

    class Meta:
        model = Doctor
        fields = (
            "id",
            "first_name",
            "last_name",
            "specialty",
            "license_number",
        )


class AppointmentPatientReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = (
            "id",
            "first_name",
            "last_name",
            "dni",
        )


class AppointmentSerializer(serializers.ModelSerializer):

    # POST / PATCH
    doctor = AppointmentDoctorSerializer(
        write_only=True
    )

    patient = AppointmentPatientSerializer(
        write_only=True
    )


    # GET
    doctor_detail = AppointmentDoctorReadSerializer(
        source="doctor",
        read_only=True,
    )

    patient_detail = AppointmentPatientReadSerializer(
        source="patient",
        read_only=True,
    )


    class Meta:
        model = Appointment

        fields = (
            "id",
            "doctor",
            "patient",
            "doctor_detail",
            "patient_detail",
            "date",
            "time",
            "status",
            "notes",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "status",
            "created_at",
            "updated_at",
        )


    def create(self, validated_data):

        doctor = validated_data.pop(
            "doctor"
        )["id"]

        patient_data = validated_data.pop(
            "patient"
        )


        patient, _ = Patient.objects.update_or_create(
            dni=patient_data["dni"],
            defaults={
                "first_name": patient_data["first_name"],
                "last_name": patient_data["last_name"],
                "sex": patient_data["sex"],
                "date_of_birth": patient_data["date_of_birth"],
            },
        )


        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            **validated_data,
        )


        EmailService.send_appointment_confirmation_email(
            appointment
        )


        return appointment