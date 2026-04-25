from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer,CustomTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registro exitoso"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer