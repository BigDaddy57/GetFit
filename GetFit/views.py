from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import requests
from .models import UserProfile
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth import logout

@login_required
def index(request):
    return render(request, 'pages/index.html')

@login_required
def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'pages/user_list.html', context)

def home(request):
    return render(request, 'base.html')

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
 
def logout_view(request):
    logout(request)
    return redirect('/')