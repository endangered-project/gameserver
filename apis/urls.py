from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apis.views import *

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

    path("random_question", get_random_question, name="api_get_random_question"),

    path("game/start", start_new_game, name="api_start_new_game"),
    path("game/question", get_new_question, name="api_get_new_question"),
    path("game/answer", answer_question, name="api_answer_question"),

    path("user", get_user_info, name="api_get_user_info"),
]
