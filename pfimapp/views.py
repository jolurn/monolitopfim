from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from pfimapp.models import User
from django.contrib.auth import login, logout, authenticate
# from django.db import IntegrityError
# from .forms import TaskForm

from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
from pfimapp.forms import CustomUserCreationForm

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
    
@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
        'form': AuthenticationForm
    })
    else:
        user = authenticate(request, email=request.POST['email'],password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{'form': AuthenticationForm, 'error': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('home')
