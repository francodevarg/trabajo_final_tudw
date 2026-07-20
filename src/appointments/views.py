from datetime import date

from rest_framework import generics
from rest_framework import serializers as drf_serializers
from rest_framework.permissions import IsAuthenticated

from .models import AppointmentStatus
from .serializers import AppointmentSerializer
from .services import get_appointments_for_user


class AppointmentListCreateView(
    generics.ListCreateAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = AppointmentSerializer


    def get_queryset(self):

        qs = get_appointments_for_user(
            self.request.user
        )


        date_from = self.request.query_params.get(
            "date_from"
        )

        date_to = self.request.query_params.get(
            "date_to"
        )


        if date_from:

            try:
                date.fromisoformat(date_from)

            except ValueError:
                raise drf_serializers.ValidationError(
                    {
                        "date_from":
                        "Invalid date format. Use YYYY-MM-DD."
                    }
                )


            qs = qs.filter(
                date__gte=date_from
            )


        if date_to:

            try:
                date.fromisoformat(date_to)

            except ValueError:
                raise drf_serializers.ValidationError(
                    {
                        "date_to":
                        "Invalid date format. Use YYYY-MM-DD."
                    }
                )


            qs = qs.filter(
                date__lte=date_to
            )


        return qs



    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user,
            status=AppointmentStatus.SCHEDULED
        )



class AppointmentDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = AppointmentSerializer


    def get_queryset(self):

        return get_appointments_for_user(
            self.request.user
        )