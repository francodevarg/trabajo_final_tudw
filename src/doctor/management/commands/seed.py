"""Comando de management para realizar el seed de la clínica médica."""
import json
from pathlib import Path
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from appointments.models import Appointment
from doctor.models import Insurance, Specialty

from .appointment_generator import AppointmentGenerator
from .doctor_factory import create_doctors
from .patient_factory import create_patients
from .utils import MODELS_TO_CLEAR, SeedContext, log_success

User = get_user_model()


class Command(BaseCommand):
    """Seed de la base de datos de la clínica médica."""

    help = "Realiza el seed completo de la base de datos de la clínica."

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ctx: SeedContext = SeedContext()
        self.data: Dict[str, Any] = {}

    def handle(self, *args: Any, **options: Any) -> None:
        """Orquesta la ejecución del seed."""
        self.load_data()
        self.clean_database()

        with transaction.atomic():
            self.create_roles()
            self.create_specialties()
            self.create_insurances()
            self.create_patients()
            self.create_doctors()
            self.create_appointments()

        self.print_summary()

    # ------------------------------------------------------------------ #
    # Carga y limpieza
    # ------------------------------------------------------------------ #
    def load_data(self) -> None:
        """Carga los datos desde el archivo JSON."""
        json_path = Path(__file__).parent / "data" / "seed_data.json"

        if not json_path.exists():
            raise CommandError(f"Archivo JSON no encontrado: {json_path}")

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            raise CommandError(f"Error al parsear JSON: {e}")

        self.stdout.write(log_success("Datos cargados desde JSON"))

    def clean_database(self) -> None:
        """Limpia la base de datos respetando el orden de dependencias."""
        for model in MODELS_TO_CLEAR:
            model.objects.all().delete()

        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(log_success("Base de datos limpiada"))

    # ------------------------------------------------------------------ #
    # Creación de catálogos
    # ------------------------------------------------------------------ #
    def create_roles(self) -> None:
        """Crea los grupos de roles."""
        roles = self.data.get("roles", [])
        for role_name in roles:
            group, _ = Group.objects.get_or_create(name=role_name)
            self.ctx.groups[role_name] = group

        self.stdout.write(log_success(f"{len(roles)} roles creados"))

    def create_specialties(self) -> None:
        """Crea las especialidades médicas."""
        specialties_data = self.data.get("specialties", [])
        for spec_data in specialties_data:
            specialty = Specialty.objects.create(
                name=spec_data["name"],
                slug=spec_data["slug"],
            )
            self.ctx.specialties[spec_data["name"]] = specialty

        self.stdout.write(log_success(f"{len(specialties_data)} especialidades creadas"))

    def create_insurances(self) -> None:
        """Crea las obras sociales."""
        insurances_data = self.data.get("insurances", [])
        for ins_data in insurances_data:
            insurance = Insurance.objects.create(
                name=ins_data["name"],
                slug=ins_data["slug"],
            )
            self.ctx.insurances[ins_data["name"]] = insurance

        self.stdout.write(log_success(f"{len(insurances_data)} obras sociales creadas"))

    # ------------------------------------------------------------------ #
    # Delegación a factories
    # ------------------------------------------------------------------ #
    def create_patients(self) -> None:
        """Delega la creación de pacientes al patient_factory."""
        count = create_patients(self.ctx, self.data.get("patients", []))
        self.stdout.write(log_success(f"{count} pacientes creados"))

    def create_doctors(self) -> None:
        """Delega la creación de médicos al doctor_factory."""
        count = create_doctors(self.ctx, self.data.get("doctors", []))
        self.stdout.write(log_success(f"{count} médicos creados"))

    def create_appointments(self) -> None:
        """Genera y persiste los turnos automáticamente."""
        generator = AppointmentGenerator()
        appointments = generator.generate(
            doctors=self.ctx.doctors.values(),
            patients=self.ctx.patients.values(),
            appointments_per_doctor=20,
            months=2,
        )

        Appointment.objects.bulk_create(appointments)
        self.stdout.write(log_success(f"{len(appointments)} turnos creados"))

    # ------------------------------------------------------------------ #
    # Resumen
    # ------------------------------------------------------------------ #
    def print_summary(self) -> None:
        """Imprime un resumen del seed ejecutado."""
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("RESUMEN DEL SEED")
        self.stdout.write("=" * 50)
        self.stdout.write(f"Roles: {len(self.ctx.groups)}")
        self.stdout.write(f"Especialidades: {len(self.ctx.specialties)}")
        self.stdout.write(f"Obras sociales: {len(self.ctx.insurances)}")
        self.stdout.write(f"Pacientes: {len(self.ctx.patients)}")
        self.stdout.write(f"Médicos: {len(self.ctx.doctors)}")
        self.stdout.write(f"Turnos: {Appointment.objects.count()}")
        self.stdout.write("=" * 50)
        self.stdout.write(self.style.SUCCESS("\n✓ Seed completado exitosamente"))