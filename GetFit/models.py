from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    goals = models.CharField(max_length=500, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
