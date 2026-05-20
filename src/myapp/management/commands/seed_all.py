from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    help = "Seed all application data"

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.SUCCESS("Starting full seed...")
        )

        call_command("seed_auth")

        call_command("seed_doctors")

        self.stdout.write(
            self.style.SUCCESS("All seeds executed successfully.")
        )