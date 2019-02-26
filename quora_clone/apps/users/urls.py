""" Topics - URL mapping """
from django.urls import path
from .views import (
    UserCreateView,
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    UserPasswordChangeDoneView,
    UserAccountView,
    UserRedirectView,
    UserProfileView,
)

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('my-profile/', UserAccountView.as_view(), name='account'),
    path('my-profile/password-change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('my-profile/password-change/done', UserPasswordChangeDoneView.as_view(), name='password-change-done'),
    path('redirect/', UserRedirectView.as_view(), name='redirect'),
    path('@<str:username>/profile/', UserProfileView.as_view(), name='profile'),
]
