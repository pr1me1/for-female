from django.urls import path

from apps.user import views
from apps.user.views import ValidateEmailView
from apps.user.views.login import LoginAPIView
from apps.user.views.profile import (
    ProfileModelAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    ProfileAvatarSetAPIView
)
from apps.user.views.refresh import RefreshTokenAPIView

app_name = "apps.user"

urlpatterns = [
    path('auth/send-otp/', views.SendOTPView.as_view(), name='send-otp-endpoint'),
    path("auth/validation/", ValidateEmailView.as_view(), name="validation-endpoint"),
    path("auth/login/", LoginAPIView.as_view(), name="login-endpoint"),
    path("auth/refresh/", RefreshTokenAPIView.as_view(), name="refresh-endpoint"),
    path("profile/", ProfileModelAPIView.as_view(), name="profile-endpoint"),
    path("profile/<int:user_id>/", ProfileDetailAPIView.as_view(), name="profile-detail-endpoint"),
    path('profile/list/', ProfileListAPIView.as_view(), name="profile-list-endpoint"),
    path('profile/set-avatar/', ProfileAvatarSetAPIView.as_view(), name="profile-detail-endpoint"),
]
