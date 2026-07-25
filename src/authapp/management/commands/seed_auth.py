from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = "Seed auth data"

    def create_user(self, data, group_name, is_staff=False, is_superuser=False):
        group = Group.objects.get(name=group_name)

        user, created = User.objects.get_or_create(
            email=data["email"],
            defaults={
                "username": data["username"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )

        if created:
            user.set_password(data["password"])
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Usuario creado: {user.email}"))

        self.stdout.write(self.style.SUCCESS(f"Usuario no creado: {user.email}"))
        user.groups.add(group)

        return user

    def handle(self, *args, **kwargs):
        for group_name in ("ADMIN", "DOCTOR", "CONTACT"):
            Group.objects.get_or_create(name=group_name)

        self.create_user(
            settings.USER_ADMIN,
            group_name="ADMIN",
            is_staff=True,
            is_superuser=True,
        )

        self.create_user(
            settings.USER_DOCTOR,
            group_name="DOCTOR",
        )

        self.stdout.write(
            self.style.SUCCESS("Auth seed completed.")
        )