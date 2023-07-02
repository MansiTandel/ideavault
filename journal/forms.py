
from django.forms import ModelForm
from tkinter import Widget
from pyexpat import model

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from . models import Idea, Profile
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

# Create a New user

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Log in a user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget = TextInput())
    password = forms.CharField(widget=PasswordInput())

# Post an idea

class IdeaPostForm(forms.ModelForm):

    class Meta:
        model = Idea
        fields = ['title', 'content',]
        exclude = ['user']

# Update an idea

class IdeaUpdateForm(forms.ModelForm):

    class Meta:
        model = Idea
        fields = ['title', 'content',]
        exclude = ['user']

# Update username & email

class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:

        model = User

        fields = ['username', 'email']
        exclude = ['password1', 'password2']

# Update Profile Picture

class UpdateProfileForm(forms.ModelForm):

    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}))

    class Meta:
        model = Profile
        fields = ['profile_pic']
