from django.contrib import admin
from django.urls import path, include

from api.router import drf_router

from api.views.user import CustomTokenObtainPairView

from django.contrib.auth import views as auth_views

from api.views.login import password_rest
from api.views.user import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('health_check.urls')),
    path('api/', include(drf_router.urls)),
    path('api/register/',RegisterView.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', password_rest, name='password_rest'),
]