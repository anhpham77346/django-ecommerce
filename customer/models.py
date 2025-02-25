from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username
