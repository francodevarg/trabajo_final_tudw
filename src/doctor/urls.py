from django.urls import path
from doctor.views import DoctorListCreateView, SpecialtyListView
# from .views import 

urlpatterns = [
    path('', DoctorListCreateView.as_view()),
    path("specialties", SpecialtyListView.as_view()),  
]