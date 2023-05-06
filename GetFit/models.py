from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    bio = models.CharField(max_length=500)
    date_of_birth = models.DateField()
    height = models.IntegerField()
    weight = models.IntegerField()
    goal_weight = models.IntegerField()
    daily_calorie_goal = models.IntegerField()
