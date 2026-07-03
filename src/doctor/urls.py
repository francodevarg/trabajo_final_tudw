from django.urls import path
from doctor.views import DoctorListCreateView, SpecialtyListCreateView, SpecialtyDetailView, DoctorViewSet

urlpatterns = [
    path('', DoctorListCreateView.as_view()),
    path("specialties", SpecialtyListCreateView.as_view()),
    path("specialties/<int:pk>", SpecialtyDetailView.as_view()),
    path(
        "<int:pk>/next-available-slot/",
        DoctorViewSet.as_view({"get": "next_available_slot"}),
        name="doctor-next-available-slot",
    ),
    path(
        "<int:pk>/available-slots/",
        DoctorViewSet.as_view({"get": "available_slots"}),
        name="doctor-available-slots",
    ),
]