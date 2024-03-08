"""
URL configuration for gemusaba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging

from decouple import config
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from users.views import register, logout_and_redirect

logger = logging.getLogger(__name__)

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_and_redirect, name='logout'),
    path('register/', register, name='register'),
    path('users/', include('users.urls')),
    path('', include('apps.urls')),
    path('api/', include('apis.urls'))
]

if config('ENABLE_DJANGO_ADMIN', cast=bool, default=False):
    urlpatterns.append(path('admin/', admin.site.urls))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="EndangerEd API",
        default_version='v1',
        description="API for EndangerEd game server"
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

debug_view = [
    # REST Framework's login and logout view
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += debug_view
    logger.debug(f"Debug view is enabled.")
    logger.debug(f"Enabled debug URL patterns: ")
    for url in debug_view:
        logger.debug(f" {url}")
