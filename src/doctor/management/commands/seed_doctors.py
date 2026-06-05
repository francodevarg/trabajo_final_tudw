from datetime import date, timedelta, time as time_type

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils import timezone

from doctor.models import (
    Specialty,
    Doctor,
    Availability,
    Insurance,
)
from patients.models import Patient
from appointments.models import Appointment

User = get_user_model()


class Command(BaseCommand):

    help = "Seed doctors, patients, and appointments"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.WARNING("Cleaning existing data..."))
        Appointment.objects.all().delete()
        Availability.objects.all().delete()
        Doctor.objects.all().delete()
        Patient.objects.all().delete()
        Specialty.objects.all().delete()
        Insurance.objects.all().delete()

        doctor_group, _ = Group.objects.get_or_create(name="DOCTOR")
        patient_group, _ = Group.objects.get_or_create(name="PATIENT")

        # ── Specialties ──────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS("Creating specialties..."))
        specialties = {}
        for name in [
            "Cardiología",
            "Dermatología",
            "Pediatría",
            "Neurología",
        ]:
            spec, _ = Specialty.objects.get_or_create(name=name)
            specialties[name] = spec

        # ── Insurances ───────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS("Creating insurances..."))
        insurances = {}
        for name in ["OSDE", "Swiss Medical", "Medifé", "Galeno"]:
            ins, _ = Insurance.objects.get_or_create(name=name)
            insurances[name] = ins

        # ── Patients ────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS("Creating patients..."))
        patients_data = [
            {
                "first_name": "Carlos",
                "last_name": "García",
                "dni": 12345678,
                "sex": "M",
                "date_of_birth": date(1985, 3, 15),
            },
            {
                "first_name": "Ana",
                "last_name": "Martínez",
                "dni": 23456789,
                "sex": "F",
                "date_of_birth": date(1990, 7, 22),
            },
            {
                "first_name": "Luis",
                "last_name": "Rodríguez",
                "dni": 34567890,
                "sex": "M",
                "date_of_birth": date(1978, 11, 2),
            },
            {
                "first_name": "Sofía",
                "last_name": "López",
                "dni": 45678901,
                "sex": "F",
                "date_of_birth": date(2000, 5, 10),
            },
            {
                "first_name": "Diego",
                "last_name": "Fernández",
                "dni": 56789012,
                "sex": "M",
                "date_of_birth": date(1995, 9, 28),
            },
        ]
        created_patients = []
        for pdata in patients_data:
            patient, _ = Patient.objects.get_or_create(
                dni=pdata["dni"],
                defaults=pdata,
            )
            created_patients.append(patient)

        # ── Patient Users (who book appointments) ──────────────────
        self.stdout.write(self.style.SUCCESS("Creating patient users..."))
        patient_users_data = [
            {
                "email": "carlos@example.com",
                "username": "patient1",
                "first_name": "Carlos",
            },
            {
                "email": "ana@example.com",
                "username": "patient2",
                "first_name": "Ana",
            },
            {
                "email": "luis@example.com",
                "username": "patient3",
                "first_name": "Luis",
            },
        ]
        created_users = []
        for udata in patient_users_data:
            user, created = User.objects.get_or_create(
                email=udata["email"],
                defaults={
                    "username": udata["username"],
                    "first_name": udata["first_name"],
                },
            )
            if created:
                user.set_password("patient123")
                user.groups.add(patient_group)
                user.save()
            created_users.append(user)

        # ── Doctors ────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS("Creating doctors..."))
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
                ],
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
                ],
            },
            {
                "email": "pedro@example.com",
                "username": "doctor3",
                "first_name": "Pedro",
                "last_name": "López",
                "specialty": "Pediatría",
                "license_number": "MN1001",
                "phone": "333333333",
                "insurances": ["OSDE", "Galeno"],
                "availabilities": [
                    (0, "08:00", "11:00"),
                    (3, "13:00", "17:00"),
                ],
            },
        ]

        created_doctors = []
        for ddata in doctors_data:
            user, created = User.objects.get_or_create(
                email=ddata["email"],
                defaults={
                    "username": ddata["username"],
                    "first_name": ddata["first_name"],
                    "last_name": ddata["last_name"],
                },
            )
            if created:
                user.set_password("doctor123")
                user.groups.add(doctor_group)
                user.save()

            doctor, _ = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    "specialty": specialties[ddata["specialty"]],
                    "phone": ddata["phone"],
                    "license_number": ddata["license_number"],
                    "description": f"Especialista en {ddata['specialty']}",
                },
            )

            for iname in ddata["insurances"]:
                doctor.insurances.add(insurances[iname])

            for day, start, end in ddata["availabilities"]:
                Availability.objects.get_or_create(
                    doctor=doctor,
                    day_of_week=day,
                    defaults={
                        "start_time": start,
                        "end_time": end,
                    },
                )
            created_doctors.append(doctor)

        # ── Appointments ───────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS("Creating appointments..."))
        today = timezone.localdate()
        
        # Calcular el lunes de la semana que viene
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7  # Si hoy es lunes, ir al próximo lunes
        next_monday = today + timedelta(days=days_until_monday)

        # Generar 3 citas por doctor para la semana que viene
        appointments_data = []
        
        # Doctor 1 (Juan Pérez - Cardiología): Lunes 09:00-12:00, Miércoles 14:00-18:00
        appointments_data.extend([
            {
                "user": created_users[0],
                "patient": created_patients[0],
                "doctor": created_doctors[0],
                "date": next_monday,  # Lunes
                "time": time_type(9, 0),
                "status": "scheduled",
            },
            {
                "user": created_users[1],
                "patient": created_patients[1],
                "doctor": created_doctors[0],
                "date": next_monday + timedelta(days=2),  # Miércoles
                "time": time_type(14, 30),
                "status": "scheduled",
            },
            {
                "user": created_users[2],
                "patient": created_patients[2],
                "doctor": created_doctors[0],
                "date": next_monday + timedelta(days=2),  # Miércoles
                "time": time_type(15, 30),
                "status": "confirmed",
            },
        ])
        
        # Doctor 2 (María Gómez - Dermatología): Martes 10:00-13:00, Viernes 15:00-19:00
        appointments_data.extend([
            {
                "user": created_users[0],
                "patient": created_patients[3],
                "doctor": created_doctors[1],
                "date": next_monday + timedelta(days=1),  # Martes
                "time": time_type(10, 0),
                "status": "scheduled",
            },
            {
                "user": created_users[1],
                "patient": created_patients[4],
                "doctor": created_doctors[1],
                "date": next_monday + timedelta(days=1),  # Martes
                "time": time_type(11, 0),
                "status": "confirmed",
            },
            {
                "user": created_users[2],
                "patient": created_patients[0],
                "doctor": created_doctors[1],
                "date": next_monday + timedelta(days=4),  # Viernes
                "time": time_type(16, 0),
                "status": "scheduled",
            },
        ])
        
        # Doctor 3 (Pedro López - Pediatría): Lunes 08:00-11:00, Jueves 13:00-17:00
        appointments_data.extend([
            {
                "user": created_users[0],
                "patient": created_patients[1],
                "doctor": created_doctors[2],
                "date": next_monday,  # Lunes
                "time": time_type(8, 30),
                "status": "scheduled",
            },
            {
                "user": created_users[1],
                "patient": created_patients[2],
                "doctor": created_doctors[2],
                "date": next_monday,  # Lunes
                "time": time_type(9, 30),
                "status": "scheduled",
            },
            {
                "user": created_users[2],
                "patient": created_patients[3],
                "doctor": created_doctors[2],
                "date": next_monday + timedelta(days=3),  # Jueves
                "time": time_type(14, 0),
                "status": "confirmed",
            },
        ])

        for adata in appointments_data:
            Appointment.objects.get_or_create(
                user=adata["user"],
                patient=adata["patient"],
                doctor=adata["doctor"],
                date=adata["date"],
                time=adata["time"],
                defaults={"status": adata["status"]},
            )

        # ── Summary ────────────────────────────────────────────────
        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completed: "
                f"{Patient.objects.count()} patients, "
                f"{Doctor.objects.count()} doctors, "
                f"{Appointment.objects.count()} appointments"
            )
        )