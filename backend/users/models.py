from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Add custom fields here if needed (e.g., bio, phone)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Required by Django Admin, but hidden for users

    def __str__(self):
        return self.email