from django.urls import path

from .views import (
    AppointmentListCreateView,
    AppointmentDetailView,
    AppointmentCompleteView,
    AppointmentCancelView,
    AppointmentCheckInView,
    AppointmentStartView,
    AppointmentNoShowView,
    AppointmentByUserView
)
urlpatterns = [
    path('', AppointmentListCreateView.as_view()),          # listar + crear
    path('/<int:pk>', AppointmentDetailView.as_view()),     # detalle + update + delete
    path(
        "/<int:pk>/complete",
        AppointmentCompleteView.as_view(), #Completar 
    ),
    path(
        "/<int:pk>/cancel",
        AppointmentCancelView.as_view(), #Cancelar 
    ),
    path(
        "/<int:pk>/check-in",
        AppointmentCheckInView.as_view(),#Asistencia
    ),
    path(
        "/<int:pk>/start",
        AppointmentStartView.as_view(), #En Progreso 
    ),
    path(
        "/<int:pk>/no-show",
        AppointmentNoShowView.as_view(), #NO Asistencia
    ),
    path("/user/<int:user_id>", AppointmentByUserView.as_view()),

]