from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages

from .models import Topic, TopicSubscription
from quora_clone.apps.posts.models import Question


# Create your views here.
class ListTopic(ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    context_object_name = 'topics'

    def post(self, request):
        print(request.POST)
        if self.request.is_ajax() and self.request.user.is_authenticated:
            # Different POST request
            if 'interest_rating' in request.POST:
                return self.set_interest_rating(request)
            elif 'knowledge_rating' in request.POST:
                return self.set_knowledge_rating(request)
            else:
                return self.subscribe_topic(request)
        else:
            messages.add_message(request, messages.INFO, 'You have to login for this operation')
            return reverse('users:login')

    def subscribe_topic(self, request):
        topic_id = request.POST['topic_id']
        data = {}
        try:
            subscribe_topic = TopicSubscription.objects.get_or_create(user=self.request.user,
                                                                      topic_id=topic_id)
            if subscribe_topic[1]:
                data['status'] = 'subscribed'
            else:
                TopicSubscription.objects.filter(user=self.request.user, topic=topic_id).delete()
                data['status'] = 'unsubscribed'
        except ObjectDoesNotExist:
            data['status'] = 'objectDoesNotExist'
        return JsonResponse(data)

    def set_interest_rating(self, request):
        topic_id = request.POST['topic_id']
        interest_rating = request.POST['interest_rating']
        data = {}
        try:
            topic = TopicSubscription.objects.get(user=self.request.user, topic=topic_id)
            topic.interest = int(interest_rating)
            topic.save()
            data['status'] = 'rating_saved'
        except ObjectDoesNotExist:
            data['status'] = 'objectDoesNotExist'
        return JsonResponse(data)

    def set_knowledge_rating(self, request):
        topic_id = request.POST['topic_id']
        knowledge_rating = request.POST['knowledge_rating']
        data = {}
        try:
            topic = TopicSubscription.objects.get(user=self.request.user, topic=topic_id)
            topic.knowledge = int(knowledge_rating)
            topic.save()
            data['status'] = 'rating_saved'
        except ObjectDoesNotExist:
            data['status'] = 'objectDoesNotExist'
        return JsonResponse(data)


# Create your views here.
class DetailTopic(DetailView):
    model = Topic
    template_name = 'topics/topics_detail.html'
    context_object_name = 'topic'
    slug_field = 'slug'
    slug_url_kwarg = 'topic_slug'
    extra_context = {}

    def get_context_data(self, *args, **kwargs):
        context = super(DetailTopic, self).get_context_data(*args, **kwargs)

        # topic = self.object
        # context['questions_list'] = topic.questions.all()

        context['questions_list'] = Question.objects.filter(topic=self.object).select_related('user')

        # context_questions = Question.objects.filter(topic=self.get_object())

        # context['questions_list2'] = Topic.objects.prefetch_related('questions')

        return context
