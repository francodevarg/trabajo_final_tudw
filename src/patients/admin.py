from django.contrib import admin

from patients.models import Patient, PatientUser


class PatientUserInline(admin.TabularInline):
    model = PatientUser
    extra = 1
    autocomplete_fields = ("user",)


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
    inlines = [PatientUserInline]


@admin.register(PatientUser)
class PatientUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "patient",
        "is_primary",
        "role",
    )
    list_filter = (
        "is_primary",
        "role",
    )
    search_fields = (
        "user__email",
        "patient__first_name",
        "patient__last_name",
        "patient__dni",
    )
    autocomplete_fields = ("user", "patient")
