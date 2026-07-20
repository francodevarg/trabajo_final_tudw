from django.contrib import admin
from appointments.models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "get_doctor_full_name",   # Nombre completo del doctor
        "get_doctor_specialty",   # Especialidad
        "patient",
        "date",
        "time",
        "status",
    )
    
    # Añadimos 'doctor' a los filtros para poder ver las citas de un doctor específico fácilmente
    list_filter = ("status", "date", "doctor")
    
    # Mejoramos la búsqueda para incluir nombre y apellido del doctor, no solo el username
    search_fields = (
        "user__email",
        "patient__first_name",
        "patient__last_name",
        "doctor__user__first_name",
        "doctor__user__last_name",
        "doctor__specialty", 
    )

    # Organizar el formulario de edición en secciones
    fieldsets = (
        ("Información de la Cita", {
            "fields": ("doctor", "patient", "date", "time", "status")
        }),
        ("Detalles Adicionales", {
            "fields": ("notes",),
            "classes": ("collapse",) # Se puede colapsar si está vacío
        }),
        ("Información del Sistema", {
            "fields": ("user", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    readonly_fields = ("created_at", "updated_at")

    # Métodos personalizados para mostrar datos del Doctor

    @admin.display(description="Doctor", ordering="doctor__user__last_name")
    def get_doctor_full_name(self, obj):
        """Devuelve el nombre completo del doctor o su username si no tiene nombre."""
        first_name = obj.doctor.user.first_name
        last_name = obj.doctor.user.last_name
        full_name = f"{first_name} {last_name}".strip()
        return full_name or obj.doctor.user.username

    @admin.display(description="Especialidad", ordering="doctor__specialty")
    def get_doctor_specialty(self, obj):
        """Devuelve la especialidad del doctor. 
        NOTA: Ajusta 'specialty' al nombre real del campo en tu modelo Doctor."""
        return getattr(obj.doctor, "specialty", "No especificada")