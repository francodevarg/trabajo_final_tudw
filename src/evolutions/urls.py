from django.urls import path

from .views import EvolutionCreateView, EvolutionByAppointmentView

urlpatterns = [
    path("", EvolutionCreateView.as_view()),
    path(
        "appointment/<int:appointment_id>",
        EvolutionByAppointmentView.as_view(),
        name="evolution-by-appointment",
    ),
]