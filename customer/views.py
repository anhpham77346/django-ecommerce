from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomerRegistrationForm

def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer/register.html', {'form': form})
