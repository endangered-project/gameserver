from django.urls import path

from users.views import *

urlpatterns = [
    path('settings/', settings, name='users_settings'),
    path('settings/profile', profile_settings, name='users_settings_profile'),
    path('staff_management/', staff_management, name='users_manage'),
    path('staff_management/manage/add', staff_management_add, name='users_manage_add'),
    path('staff_management/manage/edit/<int:user_id>', staff_management_edit, name='users_manage_edit'),
    path('staff_management/manage/disable/<int:user_id>', staff_management_disable, name='users_manage_disable')
]