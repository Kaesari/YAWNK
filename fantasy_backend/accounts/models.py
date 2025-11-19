from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('unspecified', 'Unspecified')
        ],
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)