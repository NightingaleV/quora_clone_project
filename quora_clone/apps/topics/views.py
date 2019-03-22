from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages

from .models import Topic, TopicSubscription


# Create your views here.
class ListTopic(ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    context_object_name = 'topics'

    def post(self, request):
        if self.request.is_ajax() and self.request.is_authenticated:
            topic_id = request.POST['topic_id']
            data = {}
            try:
                subscribe_topic = TopicSubscription.objects.get_or_create(user=self.request.user,
                                                                          topic_id=topic_id)
                if subscribe_topic[1]:
                    data['status'] = 'subscribed'
                else:
                    TopicSubscription.objects.filter(user=self.request.user, topic=topic_id)
                    data['status'] = 'unsubscribed'
            except ObjectDoesNotExist:
                data['status'] = 'objectDoesNotExist'
            return JsonResponse(data)
        else:
            messages.add_message(request, messages.INFO, 'You have to login for this operation')
            return reverse('users:login')


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
