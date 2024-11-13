from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(1)
        if form.is_valid():
            print(2)
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse

def user_delete(request):
    if request.method == 'POST':
        # 确认用户是否已登录
        if request.user.is_authenticated:
            # 删除当前登录的用户
            request.user.delete()
            # 注销用户
            logout(request)
            # 显示消息并重定向到登录页面
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('login')
        else:
            messages.error(request, 'You must be logged in to delete your account.')
            return redirect('home')
    else:
        # 如果不是 POST 请求，显示确认删除的页面
        return render(request, 'delete_account_confirm.html', {
            'cancel_url': reverse('home')
        })