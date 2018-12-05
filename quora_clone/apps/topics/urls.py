""" Topics - URL mapping """
from django.urls import path, include
from django.views.generic import TemplateView
from .views import ListTopic


app_name = 'topics'

urlpatterns = [
    path('', ListTopic.as_view())
]
