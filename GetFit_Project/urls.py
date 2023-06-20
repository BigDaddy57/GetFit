"""
URL configuration for GetFit_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from GetFit.views import following_view, group_settings, groups_list, index,home,RegisterView, unfollow_view
from django.contrib.auth.views import LoginView, LogoutView
from GetFit.views import user_list
from GetFit import views
from django.contrib.auth import views as auth_views
from GetFit.views import user_profile
from GetFit.views import follow_view, unfollow_view
from GetFit.views import search
from GetFit.views import like_post, comment_post, share_post
from GetFit.views import delete_chat





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('users/', user_list, name='user_list'),
    path('home/', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<int:user_id>/', views.user_profile, name='pages/user_profile'),
    path('user/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
    path('followers/<int:user_id>/', views.followers_view, name='followers'),
    path('following/<int:user_id>/', views.following_view, name='following'),
    path('user/<int:user_id>/follow/', follow_view, name='follow'),
    path('user/<int:user_id>/unfollow/', unfollow_view, name='unfollow'),
    path('friend/<int:user_id>/', views.following_view, name='follow'),
    path('unfriend/<int:user_id>/', views.unfollow_view, name='unfollow'),
    path('search/', views.search, name='search'),
    path('user/<int:user_id>/follow/', views.follow_view, name='follow'),
    path('user/<int:user_id>/follow/', views.follow_view, name='follow'),
    path('user/<int:user_id>/unfollow/', views.unfollow_view, name='unfollow'),
    path('user/<int:user_id>/friend/', following_view, name='friend'),
    path('user/<int:user_id>/unfriend/', unfollow_view, name='unfriend'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('newsfeed/', views.newsfeed, name='newsfeed'),
    path('newsfeed/posts/', views.posts, name='posts'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/create/', views.create_post, name='create_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/comment/', views.create_comment, name='comment'),
    path('<int:pk>/share/', share_post, name='share'),
    path('posts/like/<int:post_id>/', views.like_post, name='like_post'),
    path('posts/share/<int:post_id>/', views.share_post, name='share_post'),
    path('pages/settings/', views.settings, name='settings'),
    path('chats/', views.chat_list, name='chat_list'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('chat_detail/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('send_message/<int:chat_id>/', views.send_message, name='send_message'),
    path('chat/delete/<int:chat_id>/', delete_chat, name='delete_chat'),
    path('groups/', groups_list, name='groups_list'),
    path('groups/search/', views.groups_search, name='groups_search'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/join/', views.join_group, name='join_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('groups/<int:group_id>/settings/', group_settings, name='group_settings'),
    path('groups/<int:group_id>/kick/<int:member_id>/', views.kick_member, name='kick_member'),
    path('group/<int:group_id>/request-join/', views.join_group, name='join_group'),
    path('groups/<int:group_id>/requests/', views.group_requests, name='group_requests'),
    path('groups/<int:group_id>/requests/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('groups/<int:group_id>/requests/deny/<int:request_id>/', views.deny_request, name='deny_request'),
    path('<int:group_id>/discussions/create/', views.create_discussion, name='create_discussion'),
    path('<int:group_id>/discussions/', views.discussions_list, name='discussions_list'),
    path('<int:group_id>/discussions/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    


]