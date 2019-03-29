from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.urls import reverse
from django.contrib import messages

from django.db.models import Prefetch

from django.contrib.auth import get_user_model

from .models import Topic, TopicSubscription
from quora_clone.apps.posts.models import Question, Answer


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
            elif 'topic_id' in request.POST:
                return self.subscribe_topic(request)
            else:
                messages.add_message(request, messages.INFO, 'You have to login for this operation')
                return HttpResponseRedirect(reverse('users:login'))

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
        except IntegrityError:
            data['status'] = 'error'
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


# This could work with infinite scroll
# def get_ajax(self, *args, **kwargs):
#     context = self.get_context_data(**kwargs)
#     rendered = render_to_string(self.template_name,
#                                 context_instance=RequestContext(self.request, context))
#     return HttpResponse(rendered)

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
        # STEP 1
        # This is how it should be - easiest way, but include lot of junk data
        # context['questions_list'] = Question.objects.filter(topic=self.object).prefetch_related('answers__user')

        # STEP 2
        # context['questions_list'] = Question.objects.filter(topic=self.object).prefetch_related(
        #     Prefetch('answers', queryset=Answer.objects.all().select_related('user')))

        # STEP 3
        # Preparing queries
        questions_from_topic = Question.objects.filter(topic=self.object, answers__isnull=False).distinct()
        answers_with_related_data = Answer.data.order_by_upvotes().select_related('user').prefetch_related('upvotes',
                                                                                                           'bookmarks')
        questions_including_answers = questions_from_topic.prefetch_related(
            Prefetch('answers', queryset=answers_with_related_data)
        )

        context['questions_list'] = questions_including_answers

        return context
