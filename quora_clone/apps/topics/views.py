from django.shortcuts import render
from django.views.generic import ListView

from .models import Topic


# Create your views here.
class ListTopic(ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
