from django.contrib import admin
from .models import Availability, Doctor, Specialty
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Specialty)
admin.site.register(Availability)