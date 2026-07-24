from django.db.models import QuerySet
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import Appointment


def get_appointments_for_user(user: User) -> QuerySet[Appointment]:
    qs = Appointment.objects.select_related(
        "doctor__user",
        "doctor__specialty",
        "patient",
    ).prefetch_related(
        "doctor__insurances",
    ).order_by("date", "time")

    if user.groups.filter(name="ADMIN").exists():
        return qs

    if user.groups.filter(name="DOCTOR").exists():
        return qs.filter(doctor__user=user)

    return qs.filter(user=user)



class AppointmentStatusService:

    TRANSITIONS = {

        "PATIENT": {

            "scheduled": [
                "cancelled",
            ],

        },


        "DOCTOR": {

            "scheduled": [
                "checked_in",
                "cancelled",
                "no_show",
            ],

            "checked_in": [
                "in_progress",
            ],

            "in_progress": [
                "completed",
            ],

        },


        "ADMIN": {

            "scheduled": [
                "checked_in",
                "cancelled",
                "no_show",
            ],

            "checked_in": [
                "in_progress",
                "cancelled",
            ],

            "in_progress": [
                "completed",
            ],

        },
    }


    @classmethod
    def change_status(
        cls,
        appointment,
        new_status,
        role,
    ):

        current_status = appointment.status


        allowed_statuses = (
            cls.TRANSITIONS
            .get(role, {})
            .get(current_status, [])
        )


        if new_status not in allowed_statuses:

            raise ValidationError(
                {
                    "detail": (
                        f"Cannot change appointment "
                        f"from {current_status} "
                        f"to {new_status} "
                        f"with role {role}"
                    )
                }
            )


        appointment.status = new_status

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )


        return appointment
