from django.urls import path
from patients.views import PatientListView
urlpatterns = [
    path("", PatientListView.as_view(), name="patient-list"),
]