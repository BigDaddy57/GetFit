from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.views.generic import ListView


@login_required
def index(request):
    return render(request, 'pages/index.html')


class UserListView(ListView):
    model = UserProfile
    template_name = 'pages/user_list.html'
    context_object_name = 'users'


def home_view(request):
    return render(request, 'pages/index.html')
