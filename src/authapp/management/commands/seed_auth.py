import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Seed auth data"

    def _load_permissions(self):
        json_path = os.path.join(os.path.dirname(__file__), "permissions.json")
        with open(json_path, "r") as f:
            return json.load(f)

    def _load_users(self):
        json_path = os.path.join(os.path.dirname(__file__), "users.json")
        with open(json_path, "r") as f:
            return json.load(f)

    def _get_all_permissions(self):
        return Permission.objects.all()

    def _get_permissions_by_config(self, perm_list):
        from django.db.models import Q
        query = Q()
        for entry in perm_list:
            app_label, codename = entry.split(".")
            query |= Q(content_type__app_label=app_label, codename=codename)
        return Permission.objects.filter(query)

    def _assign_group_permissions(self, group, perm_config):
        if "*" in perm_config:
            group.permissions.set(self._get_all_permissions())
        else:
            group.permissions.set(self._get_permissions_by_config(perm_config))

    def _create_user(self, data, group, is_staff=False, is_superuser=False, grant_permissions=None):
        user, created = User.objects.get_or_create(
            email=data["email"],
            defaults={"username": data["username"]},
        )

        user.username = data["username"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(data["password"])
        user.save()

        user.groups.set([group])

        if grant_permissions:
            user.user_permissions.set(self._get_permissions_by_config(grant_permissions))
        elif is_superuser:
            user.user_permissions.set(self._get_all_permissions())
        else:
            user.user_permissions.clear()

        return user

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Auth seed iniciado..."))

        perm_config = self._load_permissions()

        self.stdout.write(self.style.SUCCESS("Creando grupos..."))
        admin_group, _ = Group.objects.get_or_create(name="ADMIN")
        doctor_group, _ = Group.objects.get_or_create(name="DOCTOR")
        patient_group, _ = Group.objects.get_or_create(name="PATIENT")

        self.stdout.write(self.style.SUCCESS("Asignando permisos a grupos..."))
        self._assign_group_permissions(admin_group, perm_config["ADMIN"])
        self.stdout.write(self.style.SUCCESS(f"  ADMIN: {admin_group.permissions.count()} permisos"))
        self._assign_group_permissions(doctor_group, perm_config["DOCTOR"])
        self.stdout.write(self.style.SUCCESS(f"  DOCTOR: {doctor_group.permissions.count()} permisos"))
        self._assign_group_permissions(patient_group, perm_config["PATIENT"])
        self.stdout.write(self.style.SUCCESS(f"  PATIENT: {patient_group.permissions.count()} permisos"))

        self.stdout.write(self.style.SUCCESS("Creando usuarios..."))

        self._create_user(
            settings.USER_ADMIN, admin_group,
            is_staff=True, is_superuser=False,
            grant_permissions=perm_config["ADMIN"],
        )
        self._create_user(settings.USER_DOCTOR, doctor_group)
        self._create_user(settings.USER_PATIENT, patient_group)

        for data in self._load_users():
            group_map = {"DOCTOR": doctor_group, "PATIENT": patient_group}
            self._create_user(data, group_map[data["group"]])

        self.stdout.write(self.style.SUCCESS("Auth seed completado."))
