from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from patients.models import Patient, PatientUser
from evolutions.models import Evolution
from patients.serializers import PatientListSerializer, PatientHistorySerializer, PatientCreateSerializer


class PatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.groups.filter(name="ADMIN").exists() or request.user.is_superuser:
            patients = Patient.objects.all()
        else:
            patients = Patient.objects.filter(
                user_links__user=request.user
            )

        patients = patients.prefetch_related(
            "user_links__user"
        ).order_by("last_name", "first_name")

        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        PatientUser.objects.create(
            user=request.user,
            patient=patient,
            role=PatientUser.Role.SELF,
            is_primary=True,
        )

        return Response(
            PatientListSerializer(patient).data,
            status=status.HTTP_201_CREATED,
        )

class SetPrimaryPatientView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, patient_id):
        try:
            target_link = PatientUser.objects.get(
                user=request.user, patient_id=patient_id
            )
        except PatientUser.DoesNotExist:
            if not Patient.objects.filter(id=patient_id).exists():
                return Response(
                    {"detail": "Patient not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {"detail": "Patient does not belong to this user."},
                status=status.HTTP_403_FORBIDDEN,
            )

        PatientUser.objects.filter(
            user=request.user, is_primary=True
        ).update(is_primary=False)

        target_link.is_primary = True
        target_link.save(update_fields=["is_primary"])

        return Response(
            {"primary_patient_id": str(patient_id)},
            status=status.HTTP_200_OK,
        )


class PatientHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PatientHistorySerializer

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]

        return (
            Evolution.objects.filter(
                appointment__patient_id=patient_id,
                appointment__doctor__user=self.request.user
            )
            .select_related(
                "appointment",
                "appointment__doctor__user",
                "appointment__doctor__specialty",
            )
            .order_by("-appointment__date")
        )