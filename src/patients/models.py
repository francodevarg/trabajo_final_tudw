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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"