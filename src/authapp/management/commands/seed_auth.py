from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):

    help = "Seed auth data"

    def handle(self, *args, **kwargs):

        groups = [
            "ADMIN",
            "DOCTOR",
            "PATIENT",
        ]

        for group_name in groups:
            Group.objects.get_or_create(
                name=group_name
            )

        admin_user, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "username": "admin",
                "first_name": "System",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            }
        )

        if created:
            admin_user.set_password("admin123")
            admin_user.save()

        self.stdout.write(
            self.style.SUCCESS("Auth seed completed.")
        )