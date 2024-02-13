from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from users.forms import UserCreationForms, ProfileSettingsForm, CreateUserForm, EditUserForm


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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def staff_management(request):
    users = User.objects.filter(is_staff=True).order_by('id')
    return render(request, 'users/manage/list.html', {
        'users': users
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def staff_management_add(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'User added successfully!')
            return redirect('users_manage')
    else:
        form = CreateUserForm()
    return render(request, 'users/manage/add.html', {
        'form': form
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def staff_management_edit(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User edited successfully!')
            return redirect('users_manage')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'users/manage/edit.html', {
        'form': form,
        'current_user': user
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def staff_management_disable(request, user_id):
    if request.user.id == user_id:
        messages.error(request, f'You cannot disable yourself!')
        return redirect('users_manage')
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'User disabled successfully!' if user.is_active else f'User enabled successfully!')
    return redirect('users_manage')
