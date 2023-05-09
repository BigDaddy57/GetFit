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
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserProfileForm
from django.http import HttpResponse


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

class RegisterView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Your account was created successfully!'

    def form_valid(self, form):
        response = super().form_valid(form)
        user_profile = UserProfile.objects.create(user=self.object)
        user_profile.save()
        return response

 
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'pages/user_profile.html', {'user': user, 'profile': profile})

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=user_id)
    else:
        form = UserProfileForm(instance=user.userprofile)
    return render(request, 'pages/edit_profile.html', {'form': form})

def followers_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    followers = User.objects.filter(id__in=user_profile.followers.all())
    return render(request, 'pages/followers.html', {'followers': followers})

def friends_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    friends = User.objects.filter(id__in=user_profile.friends.all())
    return render(request, 'pages/friends.html', {'friends': friends})

@login_required
def follow_view(request, user_id):
    """Follow a user"""
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    
    # Check if the logged-in user is trying to follow themselves
    if user_profile.user == request.user:
        messages.warning(request, "You can't follow yourself!")
        return redirect('pages/user_profile', user_id=user_id)
    
    # Add the logged-in user to the following list of the user being followed
    user_profile.following.add(request.user.id)
    user_profile.save()
    
    messages.success(request, f"You are now following {user_profile.user.username}")
    return redirect('pages/user_profile', user_id=user_id)

@login_required
def unfollow_view(request, user_id):
    """Unfollow a user"""
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    
    # Remove the logged-in user from the following list of the user being unfollowed
    user_profile.following.remove(request.user.id)
    user_profile.save()
    
    messages.success(request, f"You have unfollowed {user_profile.user.username}")
    return redirect('pages/user_profile', user_id=user_id)

@login_required
def friend(request, user_id):
    friend_user = get_object_or_404(UserProfile, id=user_id)
    if request.user.profile == friend_user:
        messages.error(request, 'You cannot friend yourself')
    else:
        request.user.profile.friends.add(friend_user)
        messages.success(request, f'You are now friends with {friend_user.user.username}')
    return redirect('GetFit:user_profile', user_id=friend_user.id)

@login_required
def unfriend(request, user_id):
    friend_user = get_object_or_404(UserProfile, id=user_id)
    request.user.profile.friends.remove(friend_user)
    messages.success(request, f'You are no longer friends with {friend_user.user.username}')
    return redirect('GetFit:user_profile', user_id=friend_user.id)