from rest_framework import serializers
from .models import Appointment
from doctor.models import Doctor
from patients.models import Patient


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.DictField(write_only=True)
    patient = serializers.DictField(write_only=True)

    class Meta:
        model = Appointment
        fields = (
            "id",
            "doctor",
            "patient",
            "date",
            "time",
            "status",
            "notes",
        )
        read_only_fields = ("status",)

    def get_doctor_detail(self, obj):
        return {
            "id": obj.doctor.id,
            "name": obj.doctor.name,
            "specialty": obj.doctor.specialty,
            "license_number": obj.doctor.license_number,
        }

    def get_patient_detail(self, obj):
        return {
            "first_name": obj.patient.first_name,
            "last_name": obj.patient.last_name,
            "dni": obj.patient.dni,
        }

    def create(self, validated_data):
        doctor_data = validated_data.pop("doctor")
        patient_data = validated_data.pop("patient")

        doctor = Doctor.objects.get(id=doctor_data["id"])
        patient, created = Patient.objects.get_or_create(
            dni=patient_data["dni"],
            defaults={
                "first_name": patient_data.get("first_name"),
                "last_name": patient_data.get("last_name"),
                "sex": patient_data.get("sex"),
                "date_of_birth": patient_data.get("date_of_birth"),
            }
        )

        if not created:
            patient.first_name = patient_data.get("first_name")
            patient.last_name = patient_data.get("last_name")
            patient.sex = patient_data.get("sex")
            patient.date_of_birth = patient_data.get("date_of_birth")
            patient.save()

        return Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            date=validated_data["date"],
            time=validated_data["time"],
            notes=validated_data.get("notes", ""),
            user=self.context["request"].user,
            status="scheduled",
        )