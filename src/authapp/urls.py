from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from authapp.views import RequestPatientAccessView,VerifyPatientAccessView, RequestOTPView, VerifyOTPView

urlpatterns = [
    path('refresh', TokenRefreshView.as_view()),    # renueva access
    path('verify', TokenVerifyView.as_view()),      # verifica token
    # Pacientes
    path(
        "request-patient-access",
        RequestPatientAccessView.as_view(),
    ),
    path(
        "verify-patient-access",
        VerifyPatientAccessView.as_view(),
    ),

    # Doctores
    path(
        "request-otp",
        RequestOTPView.as_view(),
    ),
    path(
        "verify-otp",
        VerifyOTPView.as_view(),
    ),
    path("logout", TokenBlacklistView.as_view()),   # logout     
]