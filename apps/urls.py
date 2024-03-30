from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='apps_home'),
    path('question', question_list, name='apps_question_list'),
    path('question/generator_test', question_generator_test, name='apps_question_generator_test'),
    path('question/create', question_create, name='apps_question_create'),
    path('question/<int:question_id>/edit', question_edit, name='apps_question_edit'),
    path('question/<int:question_id>/toggle', question_toggle_active, name='apps_question_toggle_active'),
    path('question_category', question_category_list, name='apps_question_category_list'),
    path('question_category/create', question_category_create, name='apps_question_category_create'),
    path('question_category/<int:category_id>/edit', question_category_edit, name='apps_question_category_edit'),
    path('text_custom_question', text_custom_question_list, name='apps_text_custom_question_list'),
    path('text_custom_question/create', text_custom_question_create, name='apps_text_custom_question_create'),
    path('text_custom_question/<int:question_id>', text_custom_question_view, name='apps_text_custom_question_view'),
    path('text_custom_question/<int:question_id>/edit', text_custom_question_edit, name='apps_text_custom_question_edit'),
    path('text_custom_question/<int:question_id>/toggle', text_custom_question_toggle_active, name='apps_text_custom_question_toggle_active'),
    path('image_custom_question', image_custom_question_list, name='apps_image_custom_question_list'),
    path('image_custom_question/create', image_custom_question_create, name='apps_image_custom_question_create'),
    path('image_custom_question/<int:question_id>', image_custom_question_view, name='apps_image_custom_question_view'),
    path('image_custom_question/<int:question_id>/edit', image_custom_question_edit, name='apps_image_custom_question_edit'),
    path('image_custom_question/<int:question_id>/toggle', image_custom_question_toggle_active, name='apps_image_custom_question_toggle_active'),
    path('game_mode', game_mode_list, name='apps_game_mode_list'),
    path('game_mode/create', game_mode_create, name='apps_game_mode_create'),
    path('game_mode/<int:game_mode_id>/edit', game_mode_edit, name='apps_game_mode_edit'),

    path('leaderboard', leaderboard, name='apps_leaderboard'),
    path('profile', profile, name='apps_profile'),
    path('profile/<int:user_id>', user_profile, name='apps_user_profile'),
    path('history/<int:game_id>', play_history, name='apps_play_history'),
]