from __future__ import annotations

from django.db.models import OuterRef, Subquery
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from appointments.models import Appointment
from patients.filters import PatientFilter
from patients.models import Patient
from patients.serializers import PatientDetailSerializer, PatientListSerializer


class PatientPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class PatientViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """ Read-oriented endpoint for browsing and inspecting patients. """

    pagination_class = PatientPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        last_appt_subquery = Subquery(
            Appointment.objects.filter(
                patient=OuterRef("pk"),
            )
            .order_by("-date", "-time")
            .values("date")[:1],
        )
        last_status_subquery = Subquery(
            Appointment.objects.filter(
                patient=OuterRef("pk"),
            )
            .order_by("-date", "-time")
            .values("status")[:1],
        )

        queryset = Patient.objects.select_related("user").annotate(
            last_appointment_date=last_appt_subquery,
            last_appointment_status=last_status_subquery,
        )

        if self.request.user.groups.filter(name="ADMIN").exists():
            pass
        elif self.request.user.groups.filter(name="DOCTOR").exists():
            from doctor.models import Doctor

            doctor = Doctor.objects.filter(user=self.request.user).first()
            if doctor is None:
                queryset = queryset.none()
            else:
                queryset = queryset.filter(
                    appointments__doctor=doctor,
                ).distinct()
        else:
            queryset = queryset.none()

        patient_filter = PatientFilter(self.request.query_params)
        return patient_filter.filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "list":
            return PatientListSerializer
        return PatientDetailSerializer

    def get_permissions(self):
        if self.request.user and self.request.user.groups.filter(name="ADMIN").exists():
            return [AllowAny()]
        return [IsAuthenticated()]
