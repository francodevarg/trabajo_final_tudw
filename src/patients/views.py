from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from patients.models import Patient
from evolutions.models import Evolution
from patients.serializers import PatientListSerializer,PatientHistorySerializer


class PatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.select_related("user").order_by(
            "last_name", "first_name"
        )
        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)



class PatientHistoryView(ListAPIView):
    serializer_class = PatientHistorySerializer

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]

        return (
            Evolution.objects.filter(
                appointment__patient_id=patient_id
            )
            .select_related(
                "appointment",
                "appointment__doctor__user",
                "appointment__doctor__specialty",
            )
            .order_by("-appointment__date")
        )