from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Doctor, Specialty
from .serializers import SpecialtySerializer, NextAvailableSlotSerializer, AvailableSlotSerializer
from .permissions import IsAdminRole
from .services import SlotService
from rest_framework.permissions import AllowAny


from doctor.serializers import (
    DoctorReadSerializer,
    DoctorCreateSerializer,
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

class DoctorListCreateView(APIView):
    def get_permissions(self):

        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                IsAdminRole(),
            ]

        return [AllowAny()]
    
    def get_serializer_class(self):

        if self.request.method == "POST":
            return DoctorCreateSerializer

        return DoctorReadSerializer

    def get(self, request):

        doctors = Doctor.objects.prefetch_related(
            "insurances",
            "availabilities",
        ).select_related(
            "user",
            "specialty",
        )

        serializer = self.get_serializer_class()(
            doctors,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = self.get_serializer_class()(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        doctor = serializer.save()

        response_serializer = DoctorReadSerializer(
            doctor
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class SpecialtyListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        specialties = Specialty.objects.all().values('id', 'name', 'slug')
        return Response(specialties, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = SpecialtySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=201)