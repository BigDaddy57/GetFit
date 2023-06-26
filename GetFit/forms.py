from django import forms
from django.contrib.auth.models import User
from .models import Breakfast, Dinner, Lunch, NutritionGoal, Snacks, UserProfile, WaterIntake
from .models import Post
from .models import Group
from .models import Discussion
from .models import FoodEntry

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio', 'age', 'height', 'weight', 'goals')

    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'name': 'profile_picture'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'name': 'bio'}))
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'name': 'age'}))
    height = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'name': 'height'}))
    weight = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'name': 'weight'}))
    goals = forms.CharField(required=False, widget=forms.Textarea(attrs={'name': 'goals'}))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class CreateCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=500)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

class GroupSettingsForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'privacy']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content', 'video', 'image']

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['food', 'date', 'time', 'meal_type', 'portion_size']

class WaterIntakeForm(forms.ModelForm):
    class Meta:
        model = WaterIntake
        fields = ['amount']

class BreakfastForm(forms.ModelForm):
    class Meta:
        model = Breakfast
        fields = ['foods']

class LunchForm(forms.ModelForm):
    class Meta:
        model = Lunch
        fields = ['foods']

class DinnerForm(forms.ModelForm):
    class Meta:
        model = Dinner
        fields = ['foods']

class SnacksForm(forms.ModelForm):
    class Meta:
        model = Snacks
        fields = ['foods']

class NutritionGoalForm(forms.ModelForm):
    class Meta:
        model = NutritionGoal
        fields = ['target_calories', 'target_protein', 'target_carbohydrates', 'target_fats']

