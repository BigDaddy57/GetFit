from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    goals = models.CharField(max_length=500, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    posts_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes')
def update_like_count(post_id):
    post = Post.objects.get(id=post_id)
    post.likes += 1
    post.save()
def update_comment_count(post_id):
    post = Post.objects.get(id=post_id)
    post.comments += 1
    post.save()
def update_share_count(post_id):
    post = Post.objects.get(id=post_id)
    post.shares += 1
    post.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    is_group_chat = models.BooleanField(default=False)
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, related_name='chat_last_message')
    unread_messages = models.PositiveIntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message by {self.sender.username} in {self.chat.title}'

class Group(models.Model):
    PRIVACY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('invitation', 'Invitation-only'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='group_memberships')
    created_at = models.DateTimeField(auto_now_add=True)
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    is_public = models.BooleanField(default=False)
    invited_users = models.CharField(max_length=255, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_of')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new instances
            super().save(*args, **kwargs)
            self.admin = self.members.first()  # Assign the first member as admin
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)




class JoinRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    )

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Join request for {self.group.name} by {self.user.username}"

class Discussion(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='discussions/videos', null=True, blank=True)
    image = models.ImageField(upload_to='discussions/images', null=True, blank=True)

    def __str__(self):
        return self.title

class Food(models.Model):
    name = models.CharField(max_length=200)
    calories = models.FloatField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    fats = models.FloatField()
    
    def __str__(self):
        return self.name
    
class FoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    meal_type = models.CharField(max_length=200)
    portion_size = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.user.username} - {self.food.name} - {self.date} - {self.time}'
    
class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()  # in liters

    def __str__(self):
        return f'{self.user.username} - {self.amount}L - {self.date}'

class Breakfast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return f'{self.user.username} - Breakfast - {self.date}'

class Lunch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return f'{self.user.username} - Lunch - {self.date}'

class Dinner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return f'{self.user.username} - Dinner - {self.date}'

class Snacks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return f'{self.user.username} - Snacks - {self.date}'
    
class NutritionGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_calories = models.FloatField()
    target_protein = models.FloatField()
    target_carbohydrates = models.FloatField()
    target_fats = models.FloatField()
    # Add fields for other nutrients as needed



