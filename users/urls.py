from django.urls import path

from users.views import *

urlpatterns = [
    path('settings/', settings, name='users_settings'),
    path('settings/profile', profile_settings, name='users_settings_profile'),
    path('staff_management/', staff_management, name='staff_manage'),
    path('staff_management/manage/add', staff_management_add, name='staff_manage_add'),
    path('staff_management/manage/edit/<int:user_id>', staff_management_edit, name='staff_manage_edit'),
    path('staff_management/manage/disable/<int:user_id>', staff_management_disable, name='staff_manage_disable'),
    path('users_management/', users_management, name='users_management'),
    path('users_management/manage/<int:user_id>', users_management_detail, name='users_management_detail'),
]