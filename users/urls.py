from django.urls import path

from users.views import *

urlpatterns = [
    path('settings/', settings, name='users_settings'),
    path('settings/profile', profile_settings, name='users_settings_profile')
]