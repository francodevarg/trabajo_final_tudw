from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.shortcuts import get_object_or_404

from .models import Doctor, Specialty, Insurance
from .serializers import SpecialtySerializer, InsuranceSerializer, NextAvailableSlotSerializer, AvailableSlotSerializer
from .permissions import IsAdminRole,IsAdminOrOwner
from .services import SlotService
from myapp.services.email_service import EmailService
from rest_framework.permissions import AllowAny


from doctor.serializers import (
    DoctorReadSerializer,
    DoctorCreateSerializer,
    DoctorUpdateSerializer,
)


class DoctorViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"], url_path="next-available-slot")
    def next_available_slot(self, request, pk=None):
        doctor = get_object_or_404(
            Doctor.objects.prefetch_related("availabilities"),
            pk=pk,
        )
        result = SlotService.get_next_available_slot(doctor)
        if result is None:
            return Response(
                {"detail": "No available slots found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = NextAvailableSlotSerializer(data=result)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="available-slots")
    def available_slots(self, request, pk=None):
        date_str = request.query_params.get("date")
        if not date_str:
            raise serializers.ValidationError(
                {"date": "This query parameter is required."}
            )
        try:
            target_date = date.fromisoformat(date_str)
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                {"date": "Invalid date format. Use YYYY-MM-DD."}
            )

        doctor = get_object_or_404(
            Doctor.objects.prefetch_related("availabilities"),
            pk=pk,
        )
        slots = SlotService.get_available_slots(doctor, target_date)
        serializer = AvailableSlotSerializer(data=slots, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class DoctorListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DoctorCreateSerializer
        return DoctorReadSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminRole()]
        return [AllowAny()]

    def get_queryset(self):
        return Doctor.objects.prefetch_related(
            "insurances",
            "availabilities",
        ).select_related(
            "user",
            "specialty",
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        doctor = serializer.save()
        try:
            EmailService.send_doctor_welcome_email(doctor)
        except Exception:
            pass
        read_serializer = DoctorReadSerializer(doctor)
        self.created_data = read_serializer.data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            self.created_data,
            status=status.HTTP_201_CREATED
        )


class DoctorDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return DoctorUpdateSerializer
        return DoctorReadSerializer

    def get_queryset(self):
        return Doctor.objects.prefetch_related(
            "insurances",
            "availabilities",
        ).select_related(
            "user",
            "specialty",
        )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        doctor = serializer.save()
        read_serializer = DoctorReadSerializer(doctor)
        self.updated_data = read_serializer.data

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(self.updated_data)


class SpecialtyListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminRole()]
        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SpecialtyDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class InsuranceListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminRole()]
        return [AllowAny()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class InsuranceDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)