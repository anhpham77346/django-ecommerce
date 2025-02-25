from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomerCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Đăng nhập tự động sau khi đăng ký thành công
            login(request, user)
            return redirect('home')  # Chuyển hướng đến trang chủ hoặc trang nào khác bạn muốn
    else:
        form = CustomerCreationForm()
    return render(request, 'customer/register.html', {'form': form})
