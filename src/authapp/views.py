from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from authapp.services.otp_service import OTPService
from authapp.services.patient_service import PatientService
from .serializers import RequestPatientAccessSerializer,VerifyPatientAccessSerializer,CustomTokenSerializer, RequestOTPSerializer, VerifyOTPSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User,Group
from authapp.models import Profile

# Create your views here.
class RequestPatientAccessView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RequestPatientAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user, created = PatientService.get_or_create(email)

        OTPService.create_otp_for_user(user)

        return Response(
            {
                "detail": "OTP sent successfully.",
                "created": created,
            },
            status=status.HTTP_200_OK,
        )
    
class VerifyPatientAccessView(APIView):

    authentication_classes = []
    permission_classes = []

    @staticmethod
    def error(code: str, detail: str,
              status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "code": code,
                "detail": detail,
            },
            status=status_code,
        )

    def post(self, request):
        serializer = VerifyPatientAccessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.error(
                "USER_NOT_FOUND",
                "No existe una cuenta con ese email.",
            )

        if not OTPService.validate_otp(user, otp):
            return self.error(
                "OTP_INVALID",
                "El código es inválido o expiró.",
            )

        refresh = CustomTokenSerializer.get_token(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )
    
class RequestOTPView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                {
                    "email": "Doctor not found."
                }
            )

        if not user.groups.filter(name__in=["DOCTOR", "ADMIN"]).exists():
            raise ValidationError(
                {
                    "email": "Only Doctors or Administrators can request an OTP."
                }
            )

        OTPService.create_otp_for_user(user)

        return Response(
            {
                "detail": "OTP sent successfully.",
            },
            status=status.HTTP_200_OK,
        )
    
class VerifyOTPView(APIView):

    authentication_classes = []
    permission_classes = []

    @staticmethod
    def error(code: str, detail: str,
              status_code=status.HTTP_400_BAD_REQUEST):
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

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.error(
                "USER_NOT_FOUND",
                "No existe una cuenta con ese email.",
            )

        if not OTPService.validate_otp(user, otp):
            return self.error(
                "OTP_INVALID",
                "El código es inválido o expiró.",
            )

        refresh = CustomTokenSerializer.get_token(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )