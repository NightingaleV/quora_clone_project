from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Topic


# Create your views here.
class ListTopic(ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    context_object_name = 'topics'


# Create your views here.
class DetailTopic(DetailView):
    model = Topic
    template_name = 'topics/topics_detail.html'
    context_object_name = 'topic'
    slug_field = 'slug'
    slug_url_kwarg = 'topic_slug'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailTopic, self).get_context_data(**kwargs)

        return context
