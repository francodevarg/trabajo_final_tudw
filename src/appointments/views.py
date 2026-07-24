from datetime import date

from rest_framework import generics
from rest_framework import serializers as drf_serializers
from rest_framework.permissions import IsAuthenticated

from .models import AppointmentStatus
from .serializers import AppointmentSerializer
from .services import get_appointments_for_user
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from appointments.serializers import AppointmentSerializer

from appointments.services import (
    get_appointments_for_user,
    AppointmentStatusService
)

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

class AppointmentStatusActionView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    status = None


    def get_role(self, user):

        if user.groups.filter(
            name="DOCTOR"
        ).exists():

            return "DOCTOR"


        if user.groups.filter(
            name="ADMIN"
        ).exists():

            return "ADMIN"


        if user.groups.filter(
            name="PATIENT"
        ).exists():

            return "PATIENT"


        return None



    def patch(
        self,
        request,
        pk
    ):

        try:

            appointment = (
                get_appointments_for_user(
                    request.user
                )
                .get(pk=pk)
            )

        except Exception:

            raise NotFound(
                "Appointment not found"
            )


        role = self.get_role(
            request.user
        )


        appointment = (
            AppointmentStatusService
            .change_status(
                appointment,
                self.status,
                role,
            )
        )


        return Response(
            AppointmentSerializer(
                appointment
            ).data
        )



class AppointmentCompleteView(
    AppointmentStatusActionView
):

    status = "completed"



class AppointmentCancelView(
    AppointmentStatusActionView
):

    status = "cancelled"



class AppointmentCheckInView(
    AppointmentStatusActionView
):

    status = "checked_in"



class AppointmentStartView(
    AppointmentStatusActionView
):

    status = "in_progress"



class AppointmentNoShowView(
    AppointmentStatusActionView
):

    status = "no_show"