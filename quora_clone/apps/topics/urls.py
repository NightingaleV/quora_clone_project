""" Topics - URL mapping """
from django.urls import path, include
from .views import ListTopic, DetailTopic


app_name = 'topics'

urlpatterns = [
    path('', ListTopic.as_view(), name='list'),
    path('<slug:topic_slug>/', DetailTopic.as_view(), name='detail'),
    path('<slug:topic_slug>/', include('quora_clone.apps.posts.urls')),
]
