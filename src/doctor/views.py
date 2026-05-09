from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Doctor, Specialty
from .serializers import DoctorSerializer
from .permissions import IsAdminRole


class DoctorListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return None

    def get(self, request, pk):
        doctor = self.get_object(pk)
        if doctor is None:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecialtyListView(APIView):
    # permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        specialties = Specialty.objects.all().values('id', 'name')
        return Response(specialties, status=status.HTTP_200_OK)