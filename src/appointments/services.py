from django.db.models import QuerySet
from django.contrib.auth.models import User

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
