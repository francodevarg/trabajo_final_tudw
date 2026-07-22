import json
from datetime import date, time as time_type, timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import Permission


from appointments.models import Appointment
from authapp.models import Profile
from doctor.models import Availability, Doctor, Insurance, Specialty
from patients.models import Patient

User = get_user_model()

DATA_FILE = Path(__file__).resolve().parent / "seed_data.json"


class Command(BaseCommand):

    help = "Seed doctors, patients, and appointments from seed_data.json"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        data = json.loads(DATA_FILE.read_text())

        self.stdout.write(self.style.WARNING("Cleaning existing data..."))
        Appointment.objects.all().delete()
        Availability.objects.all().delete()
        Doctor.objects.all().delete()
        Patient.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        Specialty.objects.all().delete()
        Insurance.objects.all().delete()
        groups = {}

        for role_name in data["roles"].keys():
            group, _ = Group.objects.get_or_create(name=role_name)
            groups[role_name] = group

        for role_name, permissions in data["roles"].items():

            group = groups[role_name]

            if permissions == ["*"]:
                group.permissions.set(Permission.objects.all())
                continue

            django_permissions = []

            for permission in permissions:
                app_label, codename = permission.split(".")

                django_permissions.extend(
                    Permission.objects.filter(
                        content_type__app_label=app_label,
                        codename=codename,
                    )
                )

            group.permissions.set(django_permissions)
        # ── Specialties ──────────────────────────────────────────
        specialties = {}
        for name in data["specialties"]:
            spec, _ = Specialty.objects.get_or_create(name=name)
            specialties[name] = spec

        # ── Insurances ───────────────────────────────────────────
        insurances = {}
        for name in data["insurances"]:
            ins, _ = Insurance.objects.get_or_create(name=name)
            insurances[name] = ins

        # ── Patients (+ linked Users) ────────────────────────────
        self.stdout.write(self.style.SUCCESS("Creating patients..."))
        patients_by_dni: dict[int, Patient] = {}
        for p in data["patients"]:
            patient, _ = Patient.objects.get_or_create(
                dni=p["dni"],
                defaults={
                    "first_name": p["first_name"],
                    "last_name": p["last_name"],
                    "sex": p["sex"],
                    "date_of_birth": date.fromisoformat(p["date_of_birth"]),
                },
            )

            user_data = p.get("user")
            if user_data:
                user, created = User.objects.get_or_create(
                    email=user_data["email"],
                    defaults={
                        "username": user_data["email"],
                        "first_name": p["first_name"],
                        "last_name": p["last_name"],
                    },
                )
                if created:
                    user.set_password(user_data["password"])
                    user.save()
                    user.groups.add(groups["PATIENT"])
                    Profile.objects.get_or_create(
                        user=user,
                        defaults={
                            "phone_number": "",
                            "date_of_birth": date.fromisoformat(p["date_of_birth"]),
                            "address": "",
                        },
                    )
                patient.user = user
                patient.save(update_fields=["user"])

            patients_by_dni[p["dni"]] = patient

        # ── Doctors ──────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS("Creating doctors..."))
        doctors_by_email: dict[str, Doctor] = {}
        for d in data["doctors"]:
            user, created = User.objects.get_or_create(
                email=d["email"],
                defaults={
                    "username": d["email"],
                    "first_name": d["first_name"],
                    "last_name": d["last_name"],
                },
            )
            if created:
                user.set_password(d["password"])
                user.save()
                user.groups.add(groups["DOCTOR"])

            doctor, _ = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    "consultation_fee": d["consultation_fee"],
                    "specialty": specialties[d["specialty"]],
                    "phone": d["phone"],
                    "license_number": d["license_number"],
                    "description": f"Especialista en {d['specialty']}",
                },
            )
            for iname in d["insurances"]:
                doctor.insurances.add(insurances[iname])
            for avail in d["availabilities"]:
                Availability.objects.get_or_create(
                    doctor=doctor,
                    day_of_week=avail["day"],
                    defaults={
                        "start_time": avail["start"],
                        "end_time": avail["end"],
                    },
                )
            doctors_by_email[d["email"]] = doctor

        # ── Appointments ─────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS("Creating appointments..."))
        today = timezone.localdate()
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = today + timedelta(days=days_until_monday)

        for a in data["appointments"]:
            patient = patients_by_dni[a["patient_dni"]]
            doctor = doctors_by_email[a["doctor_email"]]
            hour, minute = map(int, a["time"].split(":"))
            appt_date = next_monday + timedelta(days=a["day_offset"])

            Appointment.objects.get_or_create(
                doctor=doctor,
                date=appt_date,
                time=time_type(hour, minute),
                defaults={
                    "patient": patient,
                    "user": patient.user or User.objects.filter(is_superuser=True).first(),
                    "status": a["status"],
                },
            )

        # ── Summary ──────────────────────────────────────────────
        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completed: "
                f"{Patient.objects.count()} patients, "
                f"{Doctor.objects.count()} doctors, "
                f"{Appointment.objects.count()} appointments"
            )
        )
