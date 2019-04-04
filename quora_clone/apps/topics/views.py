from django.shortcuts import render
from django.db.models import Q, Prefetch, Sum, Count, Case, When, Value, IntegerField, Subquery, OuterRef
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Topic, TopicSubscription
from quora_clone.apps.posts.models import Question, Answer
from quora_clone.apps.posts.forms import AnswerCreationForm
from quora_clone.apps.users.models import UserFollowersBridge

User = get_user_model()


# Create your views here.
class ListTopic(ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.all().prefetch_related('subscribers')

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
        context = super(DetailTopic, self).get_context_data(**kwargs)

        # TODO maybe change sorting questions
        user_following = UserFollowersBridge.objects.filter(follower=self.request.user).values_list('following', flat=True)
        context['user_following'] = user_following

        # List of answered questions
        if not self.request.GET.get('active') or self.request.GET.get('active') == 'feed':
            questions_from_topic = Question.objects.filter(topic=self.object, answers__isnull=False,
                                                           answers__is_published__exact=True).distinct()
            answers_with_related_data = Answer.data.published().order_by_upvotes().select_related(
                'user').prefetch_related(
                'upvotes',
                'bookmarks')
            questions_including_answers = questions_from_topic.prefetch_related(
                Prefetch('answers', queryset=answers_with_related_data)
            )

            context['questions_list'] = questions_including_answers
            context['active'] = 'feed'

        # List of unanswered questions
        if self.request.GET.get('active') == 'to_answer':
            context['active'] = self.request.GET.get('active')
            context['questions_list'] = Question.data.filter(topic=self.object).count_answers().filter(
                num_answers__lt=3).already_answered_by_user(self.request.user.pk).prefetch_related('follow_question',
                                                                                                   'reminder')

        if self.request.GET.get('active') == 'contributors':
            context['active'] = self.request.GET.get('active')

            best_contributors = User.objects.filter(answers__question__topic=self.object).distinct().annotate(
                num_answers=Count('answers', distinct=True, filter=Q(answers__is_published=True))).annotate(
                num_follows=Count('follower')).annotate(
                num_upvotes=Count('answers__upvotes')).order_by('-num_upvotes')[0:10]
            context['contributors'] = best_contributors

            # # upvote_counts =
            # context['contributors'] = User.objects.filter(answers__question__topic=self.object).distinct()
            #
            # context['statistics'] = Answer.data.filter(user=self.object.pk).add_upvote_counter().aggregate(
            #     Sum('num_upvotes'))
            # context['num_answers'] = Answer.data.filter(user=self.object.pk).count()
            # context['user_followers'] = UserFollowersBridge.objects.filter(following=self.object.pk).count()

        # Add form for answering question
        # context['answer_create_form'] = AnswerCreationForm()

        return context
