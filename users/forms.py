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


class CreateUserForm(UserCreationForm):
    """Form for creating a new user."""
    is_superuser = forms.BooleanField(
        label='Create as superuser',
        help_text='Check this if you want to create this user as superuser',
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_superuser']

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.is_staff = True
        user.is_superuser = self.cleaned_data.get('is_superuser')
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    """Form for editing a user."""
    is_superuser = forms.BooleanField(
        label='Create as superuser',
        help_text='Check this if you want to create this user as superuser',
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_superuser']

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.is_staff = True
        user.is_superuser = self.cleaned_data.get('is_superuser')
        if commit:
            user.save()
        return user
