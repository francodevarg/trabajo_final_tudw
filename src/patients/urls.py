from django.urls import include, path
from rest_framework.routers import SimpleRouter

from patients.views import PatientViewSet

router = SimpleRouter()
router.register(r"", PatientViewSet, basename="patient")

urlpatterns = [
    path("", include(router.urls)),
]
