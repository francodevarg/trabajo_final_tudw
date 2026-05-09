from django.urls import path
from doctor.views import DoctorDetailView, DoctorListView, SpecialtyListView
# from .views import 

urlpatterns = [
    path('', DoctorListView.as_view()),
    path("<int:pk>/", DoctorDetailView.as_view()),  # obtiene a un doctor por id
    # path("<int:pk>/availability", DoctorDetailView.as_view()),
    path("specialties", SpecialtyListView.as_view()),  
    # path('create/', Create.as_view()),   # obtiene a
    # paht('list/', List.as_view()),   # obtiene a
    # path('update/<int:pk>/', Update.as_view()),   # obtiene a
    # path('delete/<int:pk>/', Delete.as_view()),   # obtiene a
]