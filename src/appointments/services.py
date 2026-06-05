from django.contrib.auth.models import User

from appointments.models import Appointment
from doctor.models import Doctor
from patients.models import Patient


class AppointmentService:
    @staticmethod
    def create_appointment(
        user: User,
        doctor: Doctor,
        patient: Patient,
        date,
        time,
        notes="",
    ):
        return Appointment.objects.create(
            user=user,
            doctor=doctor,
            patient=patient,
            date=date,
            time=time,
            notes=notes,
        )

    @staticmethod
    def cancel_appointment(appointment: Appointment):
        appointment.status = "cancelled"
        appointment.save(update_fields=["status"])
