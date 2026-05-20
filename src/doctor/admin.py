from django.contrib import admin
from .models import Availability, Doctor, Insurance, Specialty
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Specialty)
admin.site.register(Availability)
admin.site.register(Insurance)