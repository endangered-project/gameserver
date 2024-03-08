from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apis.views import get_random_question

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("random_question", get_random_question, name="api_get_random_question")
]
