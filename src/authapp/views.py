from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from authapp.services.otp_service import OTPService
from .serializers import RegisterSerializer,CustomTokenSerializer, RequestOTPSerializer, VerifyOTPSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

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
    
class RequestOTPView(APIView):

    def post(self, request):

        serializer = RequestOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        user, created = User.objects.get_or_create(email=email, defaults={'username': email.split('@')[0]})

        OTPService.create_otp_for_user(user)

        return Response(
            {'detail': 'OTP sent successfully.'},
            status=status.HTTP_200_OK
        )

class VerifyOTPView(APIView):

    authentication_classes = []
    permission_classes = []
    @staticmethod
    def error(code: str, detail: str, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "code": code,
                "detail": detail,
            },
            status=status_code,
        )

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = User.objects.filter(email=email).first()

        if not user:
            return self.error(
                "USER_NOT_FOUND",
                "No existe una cuenta con ese email."
            )

        if not OTPService.validate_otp(user, otp):
            return self.error(
                "OTP_INVALID",
                "El código es inválido o expiró."
            )

        refresh = CustomTokenSerializer.get_token(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=status.HTTP_200_OK,
        )