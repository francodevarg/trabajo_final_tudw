from django.conf import settings
from django.db import models


class Patient(models.Model):

    class SexChoices(models.TextChoices):
        MALE = "M", "Masculino"
        FEMALE = "F", "Femenino"
        OTHER = "O", "Otro"
        NOT_SPECIFIED = "N", "No especificado"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    dni = models.PositiveIntegerField(unique=True)
    sex = models.CharField(
        max_length=1,
        choices=SexChoices.choices,
        default=SexChoices.NOT_SPECIFIED,
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="PatientUser",
        related_name="patients",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PatientUser(models.Model):

    class Role(models.TextChoices):
        SELF = "self", "El mismo"
        PARENT = "parent", "Familiar"
        GUARDIAN = "guardian", "Responsable"
        KNOWN = "known", "Known"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_links",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="user_links",
    )
    is_primary = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SELF,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "patient"],
                name="unique_user_patient",
            ),
        ]

    def __str__(self):
        return f"{self.user.email} -> {self.patient}"
