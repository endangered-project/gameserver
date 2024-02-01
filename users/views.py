from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from users.forms import UserCreationForms, ProfileSettingsForm


def logout_and_redirect(request):
    logout(request)
    messages.success(request, f'Logged out successfully!')
    return redirect('apps_home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForms(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('apps_home')
    else:
        form = UserCreationForms()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def settings(request):
    return redirect('users_settings_profile')


@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Settings saved successfully!')
            return redirect('users_settings_profile')
    else:
        form = ProfileSettingsForm(instance=request.user.profile)
    return render(request, 'users/settings/profile.html', {'form': form})