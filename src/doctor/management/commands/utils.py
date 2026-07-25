"""Utilidades compartidas para el comando seed."""
from typing import Any, Dict, List

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from doctor.models import (
    Availability,
    Doctor,
    Insurance,
    Specialty,
)
from appointments.models import (
    Appointment
)

from patients.models import (
    Patient
)

User = get_user_model()

MODELS_TO_CLEAR: List[type] = [
    Appointment,
    Availability,
    Doctor,
    Patient,
    Specialty,
    Insurance,
]


class SeedContext:
    """Contexto compartido que almacena las entidades creadas durante el seed.

    Evita pasar diccionarios sueltos entre funciones y centraliza el acceso
    a los datos ya persistidos.
    """

    def __init__(self) -> None:
        self.groups: Dict[str, Group] = {}
        self.specialties: Dict[str, Specialty] = {}
        self.insurances: Dict[str, Insurance] = {}
        self.doctors: Dict[str, Doctor] = {}
        self.patients: Dict[str, Patient] = {}

    def reset(self) -> None:
        """Reinicia el contexto."""
        self.__init__()


def log_success(message: str) -> str:
    """Devuelve un mensaje formateado con el prefijo de éxito."""
    return f"✓ {message}"