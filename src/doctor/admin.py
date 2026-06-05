from django.contrib import admin

from authapp.models import OTPCode
from .models import Availability, Doctor, Insurance, Specialty

admin.site.register(OTPCode)

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "specialty",
        "license_number",
        "phone",
        "is_active",
        "created_at",
    )

    list_filter = (
        "specialty",
        "is_active",
        "insurances",
    )

    search_fields = (
        "user__username",
        "user__email",
        "license_number",
    )

    autocomplete_fields = (
        "user",
        "specialty",
        "insurances",
    )

    filter_horizontal = ("insurances",)

    inlines = [AvailabilityInline]

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Usuario", {
            "fields": (
                "user",
            )
        }),

        ("Información Profesional", {
            "fields": (
                "specialty",
                "license_number",
                "insurances",
            )
        }),

        ("Contacto", {
            "fields": (
                "phone",
                "description",
            )
        }),

        ("Configuración", {
            "fields": (
                "consultation_fee",
                "is_active",
            )
        }),

        ("Fechas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "day_of_week",
        "start_time",
        "end_time",
    )

    list_filter = ("day_of_week",)

    search_fields = (
        "doctor__user__username",
        "doctor__license_number",
    )