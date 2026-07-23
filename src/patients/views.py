from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient
from patients.serializers import PatientListSerializer


class PatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.select_related("user").order_by(
            "last_name", "first_name"
        )
        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)