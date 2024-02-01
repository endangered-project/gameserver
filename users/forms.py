from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile


class UserCreationForms(UserCreationForm):
    """Form for creating a new user."""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileSettingsForm(forms.ModelForm):
    """Form for profile settings page"""
    avatar = forms.ImageField(
        label='Avatar',
        help_text='Set the avatar image. (This will be resized to 500x500)',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['avatar']
