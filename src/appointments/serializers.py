from rest_framework import serializers

from .models import Appointment, AppointmentStatus
from doctor.models import Doctor, Specialty
from patients.models import Patient, PatientUser
from myapp.services.email_service import EmailService


class AppointmentDoctorSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all()
    )


class AppointmentPatientSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField(required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    dni = serializers.CharField(max_length=20, required=False)
    sex = serializers.ChoiceField(
        choices=Patient.SexChoices.choices,
        required=False,
    )
    date_of_birth = serializers.DateField(required=False)

    def validate(self, data):
        if not data.get("patient_id") and not data.get("dni"):
            raise serializers.ValidationError(
                "Se requiere patient_id o los datos del paciente (dni, first_name, last_name)."
            )
        return data


class AppointmentSpecialtyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = (
            "id",
            "name",
        )

class AppointmentDoctorReadSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )

    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )

    specialty = AppointmentSpecialtyReadSerializer(
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
            "user",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "status",
            "user",
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

        user = validated_data.pop("user")

        if patient_data.get("patient_id"):
            patient = Patient.objects.get(
                id=patient_data["patient_id"]
            )
            if not PatientUser.objects.filter(
                user=user, patient=patient
            ).exists():
                raise serializers.ValidationError(
                    {
                        "patient": "No tienes acceso a este paciente."
                    }
                )
        else:
            patient, _ = Patient.objects.update_or_create(
                dni=patient_data["dni"],
                defaults={
                    "first_name": patient_data["first_name"],
                    "last_name": patient_data["last_name"],
                    "sex": patient_data.get("sex", "N"),
                    "date_of_birth": patient_data.get("date_of_birth"),
                },
            )
            PatientUser.objects.get_or_create(
                user=user,
                patient=patient,
                defaults={"is_primary": False, "role": "self"},
            )

        overlapping = Appointment.objects.filter(
            patient=patient,
            date=validated_data["date"],
            time=validated_data["time"],
        ).exclude(status=AppointmentStatus.CANCELLED)

        if overlapping.exists():
            raise serializers.ValidationError(
                {
                    "patient": "El paciente ya tiene un turno programado a esta hora."
                }
            )

        daily_count = Appointment.objects.filter(
            patient=patient,
            date=validated_data["date"],
        ).exclude(status=AppointmentStatus.CANCELLED).count()

        if daily_count >= 3:
            raise serializers.ValidationError(
                {
                    "patient": "El paciente ya tiene el límite máximo de 3 turnos por día."
                }
            )

        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            user=user,
            **validated_data,
        )


        EmailService.send_appointment_confirmation_email(
            appointment
        )


        return appointment


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("status",)