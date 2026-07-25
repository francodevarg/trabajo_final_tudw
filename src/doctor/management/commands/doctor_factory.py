from typing import Any, Dict, List

from django.core.management.base import CommandError

from doctor.models import Availability, Doctor

from .user_factory import create_user
from .utils import SeedContext


def create_doctors(ctx: SeedContext, doctors_data: List[Dict[str, Any]]) -> int:
    """Crea todos los médicos a partir de los datos del JSON.

    Args:
        ctx: Contexto compartido del seed.
        doctors_data: Lista de diccionarios con los datos de cada médico.

    Returns:
        Cantidad de médicos creados.

    Raises:
        CommandError: Si una especialidad referenciada no existe.
    """
    for doctor_data in doctors_data:
        specialty_name: str = doctor_data.get("specialty", "")

        if specialty_name and specialty_name not in ctx.specialties:
            raise CommandError(f"Especialidad inexistente: {specialty_name}")

        user = create_user(
            ctx=ctx,
            username=doctor_data["username"],
            email=doctor_data["email"],
            first_name=doctor_data["first_name"],
            last_name=doctor_data["last_name"],
            role="DOCTOR",
        )

        doctor = Doctor.objects.create(
            user=user,
            specialty=ctx.specialties.get(specialty_name),
            license_number=doctor_data.get("license_number", ""),
            phone=doctor_data.get("phone", ""),
            consultation_fee=doctor_data.get("consultation_fee", 0),
        )

        _create_availabilities(doctor, doctor_data.get("availabilities", []))

        ctx.doctors[doctor_data["username"]] = doctor

    return len(doctors_data)


def _create_availabilities(
    doctor: Doctor, availabilities_data: List[Dict[str, Any]]
) -> None:
    """Crea las disponibilidades del médico usando bulk_create."""
    if not availabilities_data:
        return

    availabilities = [
        Availability(
            doctor=doctor,
            day_of_week=avail["day_of_week"],
            start_time=avail["start_time"],
            end_time=avail["end_time"],
        )
        for avail in availabilities_data
    ]

    Availability.objects.bulk_create(availabilities)