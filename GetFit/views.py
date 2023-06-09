from multiprocessing import context
import os
from pdb import post_mortem
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from pyparsing import FollowedBy
import requests
from GetFit_Project.settings import BASE_DIR
from .models import UserProfile, Group
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
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Post, UserProfile
from .forms import PostForm
from .forms import CreateCommentForm
from .models import Post, Comment
from .models import Post, Share
from django.http import JsonResponse
from .models import Chat, Message
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .forms import GroupForm
from GetFit.forms import GroupSettingsForm
from .models import JoinRequest
from .models import Discussion
from .forms import DiscussionForm
from django.urls import reverse

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
    user = request.user
    chats = Chat.objects.filter(participants=user) | Chat.objects.filter(is_group_chat=True)

    for chat in chats:
        last_message = chat.messages.order_by('-timestamp').first()
        chat.last_message = last_message

        if last_message:
            chat.unread_messages = chat.messages.exclude(sender=user, is_read=True).count()
        else:
            chat.unread_messages = 0

    context = {
        'chats': chats,
    }

    return render(request, 'chat/chat_list.html', context)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')

    # Retrieve the last message
    last_message = messages.last()

    # Update the last_message field of the chat
    chat.last_message = last_message
    chat.save()

    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})

# create_chat view
@login_required
def create_chat(request):
    if request.method == 'POST':
        participants = request.POST.getlist('participants')
        chat = Chat.objects.create(title='New Chat', is_group_chat=True)  # Create a group chat
        
        for participant_id in participants:
            participant = User.objects.get(id=participant_id)
            chat.participants.add(participant)
        
        chat.save()

        return redirect('chat_detail', chat_id=chat.id)
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
        chat.last_message = message
        chat.save()  # Save the chat
        return redirect('chat_detail', chat_id=chat.id)



@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Check if the current user is a participant in the chat
    if request.user not in chat.participants.all():
        raise PermissionDenied

    chat.delete()
    messages.success(request, 'Chat deleted successfully.')

    return redirect('chat_list')

@login_required
def groups_list(request):
    groups = Group.objects.filter(members=request.user)

    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            groups = groups.filter(name__icontains=query)

    return render(request, 'groups/groups_list.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.members.add(request.user)
            group.admin = request.user
            group.save()  # Save the group after setting the admin
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})


@login_required
def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    return render(request, 'groups/group_detail.html', {'group': group})


@login_required
def groups_search(request):
    query = request.GET.get('q')
    groups = Group.objects.filter(name__icontains=query)

    return render(request, 'groups/groups_search.html', {'groups': groups, 'query': query})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user = request.user

    if group.privacy == 'private':
        # Group is private, user needs to request to join
        if group.members.filter(id=user.id).exists():
            # User is already a member
            messages.warning(request, "You are already a member of this group.")
        else:
            # User is not a member, send a join request
            # (you can implement your own logic here, e.g., sending notifications to the group admin)
            messages.info(request, "Your join request has been sent to the group admin.")
    elif group.privacy == 'invitation':
        # Group is invitation-only, user needs an invitation to join
        if group.members.filter(id=user.id).exists():
            # User is already a member
            messages.warning(request, "You are already a member of this group.")
        else:
            # User is not a member, they need an invitation
            messages.info(request, "You need an invitation to join this group.")
    else:
        # Group is public, anyone can join
        if group.members.filter(id=user.id).exists():
            # User is already a member
            messages.warning(request, "You are already a member of this group.")
        else:
            # User is not a member, add them to the group
            group.members.add(user)
            messages.success(request, "You have joined the group successfully.")

    return redirect('group_detail', group_id=group_id)

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        group.delete()
        return redirect('groups_list')

    return render(request, 'groups/delete_group.html', {'group': group})

@login_required
def group_settings(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        form = GroupSettingsForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_detail', group_id=group_id)
    else:
        form = GroupSettingsForm(instance=group)

    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                if user not in group.members.all() and username not in group.invited_users.split(','):
                    # Send invitation message to the user
                    messages.success(request, f'Invitation sent successfully to {user.username}.')  # Modify the message as per your requirement
                    
                    # Save the invitation in user's chat/messages
                    invitation_message = f"You have been invited to join the group: {group.name}"
                    # You can write code here to save the invitation message to user's chat/messages

                    # Add the user to the invited_users field
                    group.invited_users += f"{username},"
                    group.save()
                else:
                    messages.error(request, 'User is already a member or has already been invited.')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')

    print(f"Group settings requested for group: {group.name}")

    context = {
        'group': group,
        'form': form,
    }
    return render(request, 'groups/group_settings.html', context)

@login_required
def kick_member(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)
    member = get_object_or_404(User, id=member_id)

    print(f"Kicking member: {member.username} from group: {group.name}")

    if request.user == group.admin:
        print("User is the group admin.")
        group.members.remove(member)
        group.save()
        messages.success(request, 'Member kicked successfully.')
    else:
        print("User is not the group admin.")
        messages.error(request, 'You do not have permission to kick members from this group.')

    return redirect(reverse('group_settings', args=[group_id]))



@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user = request.user

    if group.privacy == 'invitation':
        if not group.invitations.filter(user=user).exists():
            messages.info(request, "You need an invitation to join this group.")
            return redirect('group_detail', group_id=group_id)

    elif group.privacy == 'private':
        if group.members.filter(id=user.id).exists():
            messages.warning(request, "You are already a member of this group.")
            return redirect('group_detail', group_id=group_id)

        if group.join_requests.filter(user=user).exists():
            messages.warning(request, "You have already requested to join this group.")
            return redirect('group_detail', group_id=group_id)

        join_request = JoinRequest(group=group, user=user)
        join_request.save()
        messages.success(request, "Your join request has been sent to the group admin.")
        return redirect('group_detail', group_id=group_id)

    group.members.add(user)
    messages.success(request, "You have joined the group successfully.")
    return redirect('group_detail', group_id=group_id)


@login_required
def group_requests(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    join_requests = group.join_requests.filter(status='pending')  # Exclude accepted requests
    num_requests = join_requests.count()

    context = {
        'group': group,
        'join_requests': join_requests,
        'num_requests': num_requests,
    }

    return render(request, 'groups/group_requests.html', context)



@login_required
def accept_request(request, group_id, request_id):
    group = get_object_or_404(Group, id=group_id)
    join_request = get_object_or_404(JoinRequest, id=request_id)

    # Only group members can accept join requests
    if request.user not in group.members.all():
        return HttpResponseForbidden("You are not a member of this group.")

    join_request.status = 'accepted'
    join_request.save()
    group.members.add(join_request.user)

    messages.success(request, f"Join request from {join_request.user.username} has been accepted.")
    return redirect('group_requests', group_id=group_id)

@login_required
def deny_request(request, group_id, request_id):
    group = get_object_or_404(Group, id=group_id)
    join_request = get_object_or_404(JoinRequest, id=request_id)

    # Only group members can deny join requests
    if request.user not in group.members.all():
        return HttpResponseForbidden("You are not a member of this group.")

    join_request.status = 'denied'
    join_request.save()
    join_request.delete()

    messages.success(request, f"Join request from {join_request.user.username} has been denied.")
    return redirect('group_requests', group_id=group_id)

@login_required
def create_discussion(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.group = group
            discussion.author = request.user
            discussion.save()
            return redirect('group_detail', group_id=group_id)
    else:
        form = DiscussionForm()

    return render(request, 'groups/create_discussion.html', {'group': group, 'form': form})

@login_required
def discussions_list(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    discussions = group.discussions.all()

    return render(request, 'groups/discussions_list.html', {'group': group, 'discussions': discussions})

@login_required
def discussion_detail(request, group_id, discussion_id):
    group = get_object_or_404(Group, id=group_id)
    discussion = get_object_or_404(Discussion, id=discussion_id, group=group)

    return render(request, 'groups/discussion_detail.html', {'group': group, 'discussion': discussion})