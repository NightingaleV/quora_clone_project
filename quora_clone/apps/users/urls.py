""" Topics - URL mapping """
from django.urls import path
from .views import (
    UserCreateView,
    UserLoginView,
    UserLogoutView,
    UserChangePasswordView,
    UserChangePasswordDoneView,
    UserAccountView,
    UserRedirectView,
    UserProfileView,
)

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-change/', UserChangePasswordView.as_view(), name='change-password'),
    path('password-change/done', UserChangePasswordDoneView.as_view(), name='change-password-done'),
    path('redirect/', UserRedirectView.as_view(), name='redirect'),
    path('my-profile/', UserAccountView.as_view(), name='account'),
    path('@<str:username>/profile/', UserProfileView.as_view(), name='profile'),
]
