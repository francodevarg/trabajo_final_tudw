from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings # Importar el modelo de Usuario
# Create your models here.

class Insurance(models.Model):
    name = models.CharField(
        unique=True,
        max_length=100
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Doctor(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )

    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name="doctors"
    )

    insurances = models.ManyToManyField(
        Insurance,
        related_name="doctors",
        blank=True
    )

    license_number = models.CharField(
        max_length=50,
        unique=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    description = models.TextField(blank=True)

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    
    appointment_duration = models.PositiveIntegerField(
        default=30
    )
    
    def __str__(self):
        return (
            f"{self.user.first_name} "
            f"{self.user.last_name}"
        )
    
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

