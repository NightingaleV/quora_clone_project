""" Topics - URL mapping """
from django.urls import path, include
from django.views.generic import TemplateView
from .views import ListTopic, DetailTopic


app_name = 'topics'

urlpatterns = [
    path('', ListTopic.as_view(), name='list'),
    path('<slug:topic_slug>', DetailTopic.as_view(), name='detail')
]
