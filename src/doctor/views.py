from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Doctor, Specialty
from .serializers import SpecialtySerializer
from .permissions import IsAdminRole
from rest_framework.permissions import AllowAny


from doctor.serializers import (
    DoctorReadSerializer,
    DoctorCreateSerializer,
)

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