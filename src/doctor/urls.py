from django.urls import path
from doctor.views import DoctorListCreateView, SpecialtyListView, DoctorViewSet

urlpatterns = [
    path('', DoctorListCreateView.as_view()),
    path("specialties", SpecialtyListView.as_view()),
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