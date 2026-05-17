from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Specialty(models.Model):
    name = models.CharField(unique=True, max_length=100)
    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="doctors")
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Availability(models.Model):
    WEEK_DAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )

    day_of_week = models.IntegerField(choices=WEEK_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        # evitar solapamientos
        overlapping = Availability.objects.filter(
            doctor=self.doctor,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("La disponibilidad se superpone con otra.")

        if self.start_time >= self.end_time:
            raise ValidationError("El horario de inicio debe ser menor al de fin.")

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week} {self.start_time}-{self.end_time}"

