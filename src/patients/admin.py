from django.contrib import admin

from patients.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "dni",
        "sex",
        "date_of_birth",
    )
    search_fields = (
        "first_name",
        "last_name",
        "dni",
    )
