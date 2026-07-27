from django.urls import path
from patients.views import PatientListView, PatientHistoryView, SetPrimaryPatientView

urlpatterns = [
    path("", PatientListView.as_view(), name="patient-list"),
    path(
        "/<int:patient_id>/set-primary",
        SetPrimaryPatientView.as_view(),
        name="set-primary-patient",
    ),
    path(
        "/<int:patient_id>/history",
        PatientHistoryView.as_view(),
        name="patient-history",
    ),
]