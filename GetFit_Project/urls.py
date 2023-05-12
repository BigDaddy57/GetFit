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
from GetFit.views import friends_view, index,home,RegisterView, unfriend
from django.contrib.auth.views import LoginView, LogoutView
from GetFit.views import user_list
from GetFit import views
from django.contrib.auth import views as auth_views
from GetFit.views import user_profile
from GetFit.views import follow_view, unfollow_view
from GetFit.views import search
from GetFit.views import like_post, comment_post, share_post



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
    path('friends/<int:user_id>/', views.friends_view, name='friends'),
    path('user/<int:user_id>/follow/', follow_view, name='follow'),
    path('user/<int:user_id>/unfollow/', unfollow_view, name='unfollow'),
    path('friend/<int:user_id>/', views.friends, name='friend'),
    path('unfriend/<int:user_id>/', views.unfriend, name='unfriend'),
    path('search/', views.search, name='search'),
    path('user/<int:user_id>/follow/', views.follow_view, name='follow'),
    path('user/<int:user_id>/follow/', views.follow_view, name='follow'),
    path('user/<int:user_id>/unfollow/', views.unfollow_view, name='unfollow'),
    path('user/<int:user_id>/friend/', friends_view, name='friend'),
    path('user/<int:user_id>/unfriend/', unfriend, name='unfriend'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('newsfeed/', views.newsfeed, name='newsfeed'),
    path('newsfeed/posts/', views.posts, name='posts'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/create/', views.create_post, name='create_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/comment/', views.create_comment, name='comment'),
    path('<int:pk>/share/', share_post, name='share'),
]


