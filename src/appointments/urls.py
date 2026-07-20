from django.urls import path

from appointments.views import (
    AppointmentListCreateView,
    AppointmentDetailView,
)

urlpatterns = [
    path('', AppointmentListCreateView.as_view()),          # listar + crear
    path('/<int:pk>', AppointmentDetailView.as_view()),     # detalle + update + delete
]