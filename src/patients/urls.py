from django.urls import path
from patients.views import PatientListView,PatientHistoryView
urlpatterns = [
    path("", PatientListView.as_view(), name="patient-list"),
    path(
        "<int:patient_id>/history",
        PatientHistoryView.as_view(),
        name="patient-history",
    ),
]