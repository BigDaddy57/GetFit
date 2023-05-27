from multiprocessing import context
import os
from pdb import post_mortem
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from pyparsing import FollowedBy
import requests
from GetFit_Project.settings import BASE_DIR
from .models import  UserProfile
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
from django.http import Http404, HttpResponse
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Post, UserProfile
from .forms import PostForm
from .forms import CreateCommentForm
from .models import Post, Comment
from .models import Post, Share
from django.http import JsonResponse
from .models import Chat, Message
from django.core.exceptions import PermissionDenied


@login_required
def index(request):
    return render(request, 'pages/index.html')

@login_required
def user_list(request):
    users = User.objects.all().exclude(id=request.user.id)
    profiles = UserProfile.objects.all()
    follows = []
    friends = []
    for user in users:
        try:
            profile = user.userprofile
            follows.append(profile.followers.filter(id=request.user.id).exists())
            friends.append(profile.friends.filter(id=request.user.id).exists())
        except:
            follows.append(False)
            friends.append(False)
    return render(request, 'pages/user_list.html', {'users': zip(users, profiles, follows, friends)})

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)
    user_profile = UserProfile.objects.get(user_id=user_id)
    post_count = user_profile.posts_count
    follower_count = user_profile.followers_count
    following_count = user_profile.following_count
    return render(request, 'pages/user_profile.html', {'user': user, 'profile': profile})

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('pages/user_profile', user_id=user_id)
    else:
        form = UserProfileForm(instance=user.userprofile)
    return render(request, 'pages/edit_profile.html', {'form': form})

@login_required
def followers_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    followers = User.objects.filter(id__in=user_profile.followers.all())
    return render(request, 'pages/followers.html', {'followers': followers})

@login_required
def following_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    following = User.objects.filter(id__in=user_profile.following.all())
    return render(request, 'pages/following.html', {'following': following})

@login_required
def follow_view(request, user_id):
    """Follow a user"""
    print("Follow view called!")
    user_profile = get_object_or_404(UserProfile, user_id=user_id)

    # Check if the logged-in user is trying to follow themselves
    if user_profile.user == request.user:
        messages.warning(request, "You can't follow yourself!")
        return redirect('pages/user_profile', user_id=user_id)

    # Add the logged-in user to the following list of the user being followed
    user_profile.following.add(request.user.id)
    user_profile.save()

    # Create a Follow object to save the follower and the followed user
    follow =follow(follower=request.user, followed=user_profile.user)
    follow.save()

    messages.success(request, f"You are now following {user_profile.user.username}")
    user_profile.save()
    return redirect('pages/user_profile', user_id=user_id)

@login_required
def unfollow_view(request, user_id):
    """Unfollow a user"""
    user_profile = get_object_or_404(UserProfile, user_id=user_id)

    # Remove the logged-in user from the following list of the user being unfollowed
    user_profile.following.remove(request.user.id)
    user_profile.save()

    # Delete the Follow object of the follower and the followed user
    follow.objects.filter(follower=request.user, followed=user_profile.user).delete()

    messages.success(request, f"You have unfollowed {user_profile.user.username}")
    return redirect('pages/user_profile', user_id=user_id)

@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        results = User.objects.filter(username__icontains=query)
    else:
        results = []
    return render(request, 'pages/search_results.html', {'users': results, 'query': query})

@login_required
def newsfeed(request):
    posts = Post.objects.all().order_by('-timestamp')
    for post in posts:
        post.like_count = post.likes.count()
    return render(request, 'pages/newsfeed.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Update user profile statistics
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.num_posts += 1
            user_profile.save()

            return redirect('pages/newsfeed')
    else:
        form = PostForm()

    return render(request, 'pages/create_post.html', {'form': form})

@login_required
def posts(request):
    return render(request, 'getfit/posts/posts.html')

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            comment = Comment(user=request.user, post=post, content=content)
            comment.save()

            return redirect('newsfeed')

    else:
        form = CreateCommentForm()

    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'posts/create_comment.html', context)


@login_required
def share_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        share = Share(user=request.user, post=post)
        share.save()
        return redirect('newsfeed')
    else:
        return redirect('post_detail', post_id=post_id)
    
@login_required
def share_post(request, post_id):
    # Retrieve the post object using the post_id parameter
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        # Create a new Share object with the user and post from the request
        share = Share(user=request.user, post=post)
        share.save()
        messages.success(request, 'Post shared successfully!')
        
    # Redirect the user back to the newsfeed page
    return redirect('newsfeed')
    return JsonResponse({})
    
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the user has already liked this post
    if post.likes.filter(id=request.user.id).exists():
        # User has already liked this post, remove the like
        post.likes.remove(request.user)
        like_added = False
    else:
        # User hasn't liked this post yet, add the like
        post.likes.add(request.user)
        like_added = True

    # Create a dictionary to return as JSON response
    data = {
        'like_added': like_added,
        'num_likes': post.likes.count()
    }

    return JsonResponse(data)

@login_required
def comment_post(request):
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data['post_id']
            post = Post.objects.get(pk=post_id)
            comment = Comment(text=form.cleaned_data['text'], post=post, author=request.user)
            comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('post_detail', post_id=post_id)

    messages.error(request, 'There was an error posting your comment.')
    return redirect('home')

@login_required
def settings(request):
    return render(request, 'pages/settings.html')

@login_required
def chat_list(request):
    # Get the current user
    user = request.user

    # Retrieve the chats associated with the user
    chats = Chat.objects.filter(participants=user)

    # Create a dictionary to store the user and their chat notifications
    chat_notifications = {}

    # Iterate over the chats and group them by user
    for chat in chats:
        # Get the other participant in the chat
        other_participant = chat.participants.exclude(id=user.id).first()

        # Ensure the other participant exists
        if other_participant:
            # Add the chat to the user's notifications list
            chat_notifications.setdefault(other_participant, []).append(chat)

    context = {
        'chats': chat_notifications,
    }

    return render(request, 'chat/chat_list.html', context)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages = chat.messages.order_by('timestamp')
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})

@login_required
def create_chat(request):
    if request.method == 'POST':
        participants = request.POST.getlist('participants')
        chat = Chat.objects.create(title='New Chat')
        chat.participants.set(participants)
        return redirect('chat_detail', chat.id)
    else:
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'chat/create_chat.html', {'users': users})

@login_required
def send_message(request, chat_id):
    if request.method == 'POST':
        chat = Chat.objects.get(id=chat_id)
        sender = request.user
        content = request.POST['content']
        message = Message.objects.create(chat=chat, sender=sender, content=content)
        return redirect('chat_detail', chat_id=chat.id)

@login_required
def delete_chat(request, user_id):
    chats = Chat.objects.filter(participants__id=user_id)

    # Check if the user has permission to delete any of the chats
    chat_to_delete = None
    for chat in chats:
        if request.user in chat.participants.all():
            chat_to_delete = chat
            break

    if chat_to_delete is None:
        raise PermissionDenied

    chat_to_delete.delete()
    messages.success(request, 'Chat deleted successfully.')

    return redirect('chat_list')



