from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    address = models.CharField(max_length=255, blank=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}'s profile"