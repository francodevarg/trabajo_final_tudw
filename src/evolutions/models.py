from django.db import models

from appointments.models import Appointment


class Evolution(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="evolution",
    )

    reason = models.TextField(
        verbose_name="Motivo de consulta"
    )

    diagnosis = models.TextField(
        verbose_name="Diagnóstico"
    )

    treatment = models.TextField(
        verbose_name="Tratamiento"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Observaciones"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evolución {self.appointment_id}"