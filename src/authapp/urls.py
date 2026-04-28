from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from authapp.views import CustomTokenView, RegisterView

urlpatterns = [
    path('login/', CustomTokenView.as_view()),       # obtiene access + refresh
    path('refresh/', TokenRefreshView.as_view()),    # renueva access
    path('verify/', TokenVerifyView.as_view()),      # verifica token
    path('register/', RegisterView.as_view()),       # registro de usuario
]