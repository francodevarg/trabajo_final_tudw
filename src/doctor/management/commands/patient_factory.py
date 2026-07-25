"""Factory para la creación de pacientes."""
from typing import Any, Dict, List

from patients.models import Patient

from .user_factory import create_user
from .utils import SeedContext


def create_patients(ctx: SeedContext, patients_data: List[Dict[str, Any]]) -> int:
    """Crea todos los pacientes a partir de los datos del JSON.

    Args:
        ctx: Contexto compartido del seed.
        patients_data: Lista de diccionarios con los datos de cada paciente.

    Returns:
        Cantidad de pacientes creados.
    """
    for patient_data in patients_data:
        user = create_user(
            ctx=ctx,
            username=patient_data["username"],
            email=patient_data["email"],
            first_name=patient_data["first_name"],
            last_name=patient_data["last_name"],
            role="PATIENT",
        )

        patient = Patient.objects.create(
            user=user,
            first_name=patient_data["first_name"],
            last_name=patient_data["last_name"],
            date_of_birth=patient_data.get("date_of_birth"),
            dni=patient_data["dni"],
            sex=patient_data.get("sex", "N"),
        )

        ctx.patients[patient_data["username"]] = patient

    return len(patients_data)