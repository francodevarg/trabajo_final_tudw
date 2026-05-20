from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

from doctor.models import (
    Specialty,
    Doctor,
    Availability,
    Insurance,
)

User = get_user_model()


class Command(BaseCommand):

    help = "Seed doctors data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING("Cleaning doctors data...")
        )

        Availability.objects.all().delete()
        Doctor.objects.all().delete()
        Specialty.objects.all().delete()
        Insurance.objects.all().delete()

        doctor_group, _ = Group.objects.get_or_create(
            name="DOCTOR"
        )

        self.stdout.write(
            self.style.SUCCESS("Creating specialties...")
        )

        specialties = {
            "Cardiología": None,
            "Dermatología": None,
            "Pediatría": None,
            "Neurología": None,
        }

        for specialty_name in specialties.keys():
            specialty, _ = Specialty.objects.get_or_create(
                name=specialty_name
            )

            specialties[specialty_name] = specialty

        self.stdout.write(
            self.style.SUCCESS("Creating insurances...")
        )

        insurance_names = [
            "OSDE",
            "Swiss Medical",
            "Medifé",
            "Galeno",
        ]

        insurances = {}

        for insurance_name in insurance_names:

            insurance, _ = Insurance.objects.get_or_create(
                name=insurance_name
            )

            insurances[insurance_name] = insurance

        self.stdout.write(
            self.style.SUCCESS("Creating doctors...")
        )

        doctors_data = [
            {
                "email": "juan@example.com",
                "username": "doctor1",
                "first_name": "Juan",
                "last_name": "Pérez",
                "specialty": "Cardiología",
                "license_number": "MN1004",
                "phone": "111111111",
                "insurances": ["OSDE", "Swiss Medical"],
                "availabilities": [
                    (0, "09:00", "12:00"),
                    (2, "14:00", "18:00"),
                ]
            },
            {
                "email": "maria@example.com",
                "username": "doctor2",
                "first_name": "María",
                "last_name": "Gómez",
                "specialty": "Dermatología",
                "license_number": "MN1002",
                "phone": "222222222",
                "insurances": ["Medifé"],
                "availabilities": [
                    (1, "10:00", "13:00"),
                    (4, "15:00", "19:00"),
                ]
            },
            {
                "email": "pedro@example.com",
                "username": "doctor3",
                "first_name": "Pedro",
                "last_name": "López",
                "specialty": "Pediatría",
                "phone": "333333333",
                "license_number": "MN1001",
                "insurances": ["OSDE", "Galeno"],
                "availabilities": [
                    (0, "08:00", "11:00"),
                    (3, "13:00", "17:00"),
                ]
            },
        ]

        for doctor_data in doctors_data:

            user = User.objects.create_user(
                email=doctor_data["email"],
                username=doctor_data["username"],
                password="doctor123",
                first_name=doctor_data["first_name"],
                last_name=doctor_data["last_name"],
            )

            user.groups.add(doctor_group)

            doctor = Doctor.objects.create(
                user=user,
                specialty=specialties[
                    doctor_data["specialty"]
                ],
                phone=doctor_data["phone"],
                license_number=doctor_data["license_number"],
                description=f"""
                Especialista en {doctor_data['specialty']}
                """.strip(),
            )

            for insurance_name in doctor_data["insurances"]:
                doctor.insurances.add(
                    insurances[insurance_name]
                )

            for availability_data in doctor_data["availabilities"]:

                day_of_week, start_time, end_time = (
                    availability_data
                )

                Availability.objects.create(
                    doctor=doctor,
                    day_of_week=day_of_week,
                    start_time=start_time,
                    end_time=end_time,
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Doctors seed completed successfully."
            )
        )