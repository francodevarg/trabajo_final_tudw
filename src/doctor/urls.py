from django.urls import path
from doctor.views import (
    DoctorListCreateView,
    DoctorDetailView,
    SpecialtyListCreateView,
    SpecialtyDetailView,
    InsuranceListCreateView,
    InsuranceDetailView,
    DoctorViewSet,
)

urlpatterns = [
    path('', DoctorListCreateView.as_view(), name="doctor-list-create"),
    path("/specialties", SpecialtyListCreateView.as_view(), name="specialty-list-create"),
    path("/specialties/<int:pk>", SpecialtyDetailView.as_view(), name="specialty-detail"),
    path("/insurances", InsuranceListCreateView.as_view(), name="insurance-list-create"),
    path("/insurances/<int:pk>", InsuranceDetailView.as_view(), name="insurance-detail"),
    path(
        "/<int:pk>/next-available-slot/",
        DoctorViewSet.as_view({"get": "next_available_slot"}),
        name="doctor-next-available-slot",
    ),
    path(
        "/<int:pk>/available-slots/",
        DoctorViewSet.as_view({"get": "available_slots"}),
        name="doctor-available-slots",
    ),
    path('/<int:pk>', DoctorDetailView.as_view(), name="doctor-detail"),
]