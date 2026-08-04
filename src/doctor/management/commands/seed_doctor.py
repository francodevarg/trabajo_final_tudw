from datetime import time as time_type

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from doctor.models import Availability, Doctor, Insurance, Specialty

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the doctor profile for the USER_DOCTOR from settings/.env"

    DEFAULT_SPECIALTY = "Cardiología"
    DEFAULT_INSURANCES = ["OSDE", "Swiss Medical"]
    DEFAULT_AVAILABILITY_DAYS = [0, 1, 2, 3, 4]
    DEFAULT_START_TIME = time_type(8, 0)
    DEFAULT_END_TIME = time_type(12, 0)
    DEFAULT_FEE = 15000.00

    def _get_or_create_specialty(self):
        specialty, _ = Specialty.objects.get_or_create(name=self.DEFAULT_SPECIALTY)
        return specialty

    def _get_insurances(self):
        insurances = []
        for name in self.DEFAULT_INSURANCES:
            insurance, _ = Insurance.objects.get_or_create(name=name)
            insurances.append(insurance)
        return insurances

    def _get_user(self):
        try:
            return User.objects.get(username=settings.USER_DOCTOR["username"])
        except User.DoesNotExist:
            raise CommandError(
                f"No se encontro el usuario USER_DOCTOR "
                f"'{settings.USER_DOCTOR['username']}'. Ejecuta primero seed_auth."
            )

    def _sync_availability(self, doctor):
        for day in self.DEFAULT_AVAILABILITY_DAYS:
            Availability.objects.get_or_create(
                doctor=doctor,
                day_of_week=day,
                defaults={
                    "start_time": self.DEFAULT_START_TIME,
                    "end_time": self.DEFAULT_END_TIME,
                },
            )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Doctor seed iniciado..."))

        user = self._get_user()
        username = user.username

        doctor, created = Doctor.objects.update_or_create(
            user=user,
            defaults={
                "specialty": self._get_or_create_specialty(),
                "license_number": f"MP-{username.upper()}",
                "phone": "",
                "description": "Perfil de doctor demo creado desde USER_DOCTOR (.env).",
                "consultation_fee": self.DEFAULT_FEE,
                "is_active": True,
                "appointment_duration": 30,
            },
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Perfil de doctor creado' if created else 'Perfil de doctor actualizado'}: "
                f"{doctor} ({username})"
            )
        )

        doctor.insurances.set(self._get_insurances())
        self.stdout.write(
            self.style.SUCCESS(
                f"Obras sociales asignadas: "
                f"{', '.join(i.name for i in doctor.insurances.all())}"
            )
        )

        self._sync_availability(doctor)
        self.stdout.write(
            self.style.SUCCESS(
                f"Disponibilidad sincronizada: {doctor.availabilities.count()} dias"
            )
        )

        self.stdout.write(self.style.SUCCESS("Doctor seed completado."))
