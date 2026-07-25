from django.contrib import admin

from .models import Evolution


@admin.register(Evolution)
class EvolutionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "appointment",
        "doctor",
        "patient",
        "reason"
    )

    search_fields = (
        "appointment__doctor__user__first_name",
        "appointment__doctor__user__last_name",
        "appointment__patient__user__first_name",
        "appointment__patient__user__last_name",
        "diagnosis",
    )

    list_filter = (
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "appointment",
                    "created_at",
                )
            },
        ),
        (
            "Evolución Clínica",
            {
                "fields": (
                    "reason",
                    "diagnosis",
                    "treatment",
                    "notes",
                )
            },
        ),
    )

    @admin.display(description="Doctor")
    def doctor(self, obj):
        return obj.appointment.doctor

    @admin.display(description="Paciente")
    def patient(self, obj):
        return obj.appointment.patient