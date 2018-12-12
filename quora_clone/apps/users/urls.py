""" Topics - URL mapping """
from django.urls import path
from .views import (
    UserCreateView,
    UserLoginView,
    UserRedirectView,
    UserProfileView,
)

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('redirect/', UserRedirectView.as_view(), name='redirect'),
    path('@<str:username>/profile/', UserProfileView.as_view(), name='profile'),
]
