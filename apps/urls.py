from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='apps_home'),
    path('question', question_list, name='apps_question_list'),
    path('question/generator_test', question_generator_test, name='apps_question_generator_test'),
    path('question/create', question_create, name='apps_question_create'),
    path('question/<int:question_id>/edit', question_edit, name='apps_question_edit'),
    path('question_category', question_category_list, name='apps_question_category_list'),
    path('question_category/create', question_category_create, name='apps_question_category_create'),
    path('question_category/<int:category_id>/edit', question_category_edit, name='apps_question_category_edit'),
    path('game_mode', game_mode_list, name='apps_game_mode_list'),
    path('game_mode/create', game_mode_create, name='apps_game_mode_create'),
    path('game_mode/<int:game_mode_id>/edit', game_mode_edit, name='apps_game_mode_edit')
]