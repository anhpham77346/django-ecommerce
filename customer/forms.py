from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'birth_date', 'gender', 'password1', 'password2']
