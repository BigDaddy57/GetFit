from django.shortcuts import render
from .models import User
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def home_view(request):
    return render(request, 'index.html')

