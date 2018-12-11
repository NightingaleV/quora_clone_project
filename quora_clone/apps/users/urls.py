""" Topics - URL mapping """
from django.urls import path, include
from .views import UserCreateView

app_name = 'users'

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='registration')
]
