from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from authapp.views import RegisterView, RequestOTPView, VerifyOTPView

urlpatterns = [
    path('refresh', TokenRefreshView.as_view()),    # renueva access
    path('verify', TokenVerifyView.as_view()),      # verifica token
    path('register', RegisterView.as_view()),       # registro de usuario
    path('request-otp', RequestOTPView.as_view()),  # solicitud de OTP
    path('verify-otp', VerifyOTPView.as_view()),    # verificación de OTP
]