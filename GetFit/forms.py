from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Post
from .models import Group

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
