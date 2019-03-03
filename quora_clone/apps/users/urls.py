""" Topics - URL mapping """
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView
from .views import (
    UserCreateView,
    UserLoginView,
    UserLogoutView,
    UserUpdateView,
    UserPasswordChangeView,
    UserPasswordChangeDoneView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
    UserAccountView,
    UserRedirectView,
    UserProfileView,
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', UserCreateView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('edit/', UserUpdateView.as_view(), name='profile-edit'),
    # Password Reset
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/complete/', UserPasswordResetCompleteView.as_view(), name='password-reset-complete'),
    # Password Change
    path('password-change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password-change/done', UserPasswordChangeDoneView.as_view(), name='password-change-done'),
    path('redirect/', UserRedirectView.as_view(), name='redirect'),
    # User Profiles
    path('my-profile/', UserAccountView.as_view(), name='account'),
    path('@<str:alias>/', UserProfileView.as_view(), name='profile'),
    # path('', include('django.contrib.auth.urls')),
]
