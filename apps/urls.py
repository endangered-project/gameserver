from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='apps_home'),
    path('question', question_list, name='apps_question_list'),
    path('question/create', question_create, name='apps_question_create'),
    path('question/<int:question_id>/edit', question_edit, name='apps_question_edit'),
]