import os
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    help = "Seed all application data"

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.SUCCESS("Starting full seed...")
        )

        call_command("seed_auth")

        self.stdout.write(self.style.SUCCESS("Ejecutando seed.sql..."))

        sql_path = os.path.normpath(
            os.path.join(settings.BASE_DIR.parent, "config", "seed.sql")
        )

        if not os.path.exists(sql_path):
            self.stdout.write(self.style.ERROR(f"No se encontro {sql_path}"))
            return

        db = settings.DATABASES["default"]
        env = os.environ.copy()
        env["PGPASSWORD"] = db["PASSWORD"]

        result = subprocess.run(
            [
                "psql",
                "-h", db["HOST"],
                "-U", db["USER"],
                "-d", db["NAME"],
                "-f", sql_path,
            ],
            env=env,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            self.stdout.write(self.style.ERROR(f"Error en psql:\n{result.stderr}"))
        else:
            self.stdout.write(self.style.SUCCESS("seed.sql ejecutado correctamente."))

        self.stdout.write(
            self.style.SUCCESS("All seeds executed successfully.")
        )
