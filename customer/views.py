from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerRegistrationForm

def register_view(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer/register.html', {'form': form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = 'Tên đăng nhập hoặc mật khẩu không chính xác.'
        else:
            error_message = 'Tên đăng nhập hoặc mật khẩu không chính xác.'
    else:
        form = AuthenticationForm()
    return render(request, 'customer/login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')
