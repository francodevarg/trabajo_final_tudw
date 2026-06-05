from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

from doctor.models import (
    Availability,
    Doctor,
    Specialty,
    Insurance,
)
from appointments.models import Appointment
from patients.models import Patient

User = get_user_model()


class Command(BaseCommand):

    help = "Clear database test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING("Clearing database...")
        )

        Appointment.objects.all().delete()
        Availability.objects.all().delete()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        Specialty.objects.all().delete()
        Insurance.objects.all().delete()

        Group.objects.all().delete()

        User.objects.exclude(
            is_superuser=True
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Database cleaned successfully."
            )
        )