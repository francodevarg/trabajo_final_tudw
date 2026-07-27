import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def forward_migrate_user_links(apps, schema_editor):
    Patient = apps.get_model("patients", "Patient")
    PatientUser = apps.get_model("patients", "PatientUser")

    for patient in Patient.objects.filter(user__isnull=False):
        PatientUser.objects.get_or_create(
            user=patient.user,
            patient=patient,
            defaults={"is_primary": True, "role": "self"},
        )


def reverse_migrate_user_links(apps, schema_editor):
    Patient = apps.get_model("patients", "Patient")
    PatientUser = apps.get_model("patients", "PatientUser")

    for link in PatientUser.objects.filter(is_primary=True):
        link.patient.user = link.user
        link.patient.save(update_fields=["user"])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("patients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_primary",
                    models.BooleanField(default=False),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("self", "El mismo"),
                            ("parent", "Padre/Madre"),
                            ("guardian", "Tutor"),
                        ],
                        default="self",
                        max_length=20,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_links",
                        to="patients.patient",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_links",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="patientuser",
            constraint=models.UniqueConstraint(
                fields=("user", "patient"),
                name="unique_user_patient",
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="users",
            field=models.ManyToManyField(
                related_name="patients",
                through="patients.PatientUser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(
            forward_migrate_user_links,
            reverse_migrate_user_links,
        ),
        migrations.RemoveField(
            model_name="patient",
            name="user",
        ),
    ]
