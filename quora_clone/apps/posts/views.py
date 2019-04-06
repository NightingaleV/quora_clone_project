from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch, Sum, Max, Count, Case, When, Value, IntegerField, Subquery, OuterRef
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, FormView, CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .models import Question, Answer, Upvotes, Bookmarks, FollowQuestion, AnswerLater
from .forms import AnswerCreationForm, AnswerEditForm
from quora_clone.apps.users.models import UserFollowersBridge
from quora_clone.apps.topics.models import Topic, TopicSubscription


class CreateQuestionView(CreateView):
    pass


class DetailQuestion(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'posts/question_detail_feed.html'
    slug_field = 'slug'
    slug_url_kwarg = 'question_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        answers_list = Answer.data.filter(question=self.object).published().order_by_upvotes().select_related(
            'user').prefetch_related(
            'upvotes',
            'bookmarks')

        paginator_answers_list = Paginator(answers_list, 5)
        context['answers_list'] = paginator_answers_list.get_page(self.request.GET.get('page'))
        user_following = UserFollowersBridge.objects.filter(follower=self.request.user).values_list('following',
                                                                                                    flat=True)
        context['user_following'] = user_following

        return context


class ListAnsweredQuestion(ListView):
    model = Question
    context_object_name = 'questions_list'
    template_name = 'posts/question_list_answered.html'
    paginate_by = 15

    def get_queryset(self):
        # subscribed_topics = TopicSubscription.objects.filter(user=self.request.user).values_list('topic_id',flat=True)
        subscribed_topics = Topic.objects.subscribed_by(self.request.user).values_list('id', flat=True)
        people_followed_by_user = UserFollowersBridge.objects.filter(follower=self.request.user).values_list(
            'following',
            flat=True)
        if not self.request.GET.get('active') or self.request.GET.get('active') == 'feed':
            questions_list = Question.data.filter(topic_id__in=subscribed_topics,
                                                  answers__is_published=True).select_related('topic').distinct()
            queryset = questions_list.add_chance_to_like_a_answer(self.request.user) \
                .order_by('-num_interest', '-answers__created_at') \
                .prefetch_best_answers()

        elif self.request.GET.get('active') == 'following_questions':
            questions_list = Question.data.filter(topic_id__in=subscribed_topics,
                                                  followed_by__user=self.request.user).select_related('topic')
            queryset = questions_list.distinct().prefetch_best_answers().order_by('-followed_by__created_at')

        elif self.request.GET.get('active') == 'fav_writers':
            questions_list = Question.data.filter(topic_id__in=subscribed_topics,
                                                  answers__user__in=people_followed_by_user,
                                                  answers__is_published=True).select_related('topic')
            queryset = questions_list.add_chance_to_like_a_answer(self.request.user).order_by('-answers__created_at') \
                .prefetch_best_answers()

        elif self.request.GET.get('active') == 'bookmarks':
            user_bookmarks = Bookmarks.objects.filter(user=self.request.user).values_list('bookmark')
            questions_list = Question.data.filter(answers__in=user_bookmarks).select_related('topic')
            queryset = questions_list.distinct().prefetch_bookmarks(self.request.user).order_by('-answers__saved_by__created_at')
        else:
            queryset = Question.data.filter(topic__slug=self.request.GET.get('active')).count_answers().filter(
                num_answers__lt=3).exclude_already_answered_by_user(self.request.user.pk).prefetch_related(
                'follow_question',
                'reminder')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        user_following = UserFollowersBridge.objects.filter(follower=self.request.user).values_list('following',
                                                                                                    flat=True)
        context['user_following'] = user_following
        context['subscribed_topics'] = Topic.objects.subscribed_by(self.request.user)
        context['active'] = self.request.GET.get('active')
        if context['active'] in ['feed', 'following_questions', 'fav_writers', 'bookmarks', None]:
            context['have_answers'] = True

        return context


class ListUnansweredQuestion(ListView):
    model = Question
    context_object_name = 'questions_list'
    template_name = 'posts/question_list_unanswered.html'
    paginate_by = 15

    def get_queryset(self):
        # subscribed_topics = TopicSubscription.objects.filter(user=self.request.user).values_list('topic_id',flat=True)
        subscribed_topics = Topic.objects.subscribed_by(self.request.user)
        if not self.request.GET.get('active') or self.request.GET.get('active') == 'to_answer':
            unanswered_questions_list = Question.data.filter(
                topic__in=subscribed_topics).get_unanswered().exclude_already_answered_by_user(
                self.request.user.pk).prefetch_followers_reminders()

            queryset = unanswered_questions_list.add_chance_user_to_answer(
                self.request.user).order_by_chance_to_answer()

        elif self.request.GET.get('active') == 'reminder':
            queryset = Question.data.filter(
                to_be_reminded__user_id=self.request.user.id).prefetch_followers_reminders()

        elif self.request.GET.get('active') == 'my_concepts':
            questions_from_topic = Question.objects.filter(answers__user=self.request.user, answers__is_published=False)
            answers_with_related_data = Answer.data.unpublished().filter(user=self.request.user).select_related(
                'user')
            queryset = questions_from_topic.prefetch_related(
                Prefetch('answers', queryset=answers_with_related_data)
            )

        elif self.request.GET.get('active') == 'my_answers':
            questions_from_topic = Question.objects.filter(answers__user=self.request.user,
                                                           answers__is_published=True).distinct()
            answers_with_related_data = Answer.data \
                .published() \
                .filter(user=self.request.user) \
                .add_upvote_counter() \
                .distinct() \
                .select_related('user') \
                .prefetch_related('upvotes', 'bookmarks')

            queryset = questions_from_topic.prefetch_related(
                Prefetch('answers', queryset=answers_with_related_data)
            ).order_by('-answers__created_at')
        else:
            queryset = Question.data.filter(topic__slug=self.request.GET.get('active')).count_answers().filter(
                num_answers__lt=3).exclude_already_answered_by_user(self.request.user.pk).prefetch_related(
                'follow_question',
                'reminder')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        subscribed_topics = Topic.objects.subscribed_by(self.request.user)
        context['subscribed_topics'] = subscribed_topics
        # For labels in sidebar menu
        context['num_reminders'] = AnswerLater.objects.filter(user=self.request.user).count()
        context['num_published_by_user'] = Answer.data.filter(user=self.request.user).published().count()
        context['num_unpublished_by_user'] = Answer.data.filter(user=self.request.user).unpublished().count()

        context['active'] = self.request.GET.get('active')
        if context['active'] in ['my_answers', 'my_concepts']:
            context['have_answers'] = True
        return context


class CreateAnswer(CreateView):
    form_class = AnswerCreationForm
    template_name = 'posts/_modal_answer_create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateAnswer, self).get_context_data()
        if self.request.method == 'GET':
            context['modal_question'] = Question.objects.get(id=self.request.GET.get('question_id'))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        if self.request.is_ajax():
            self.object.save()
            data = {'status': 'success'}
            return JsonResponse(data)
        valid = super().form_valid(form)
        return valid


class EditAnswer(UpdateView):
    model = Answer
    form_class = AnswerEditForm
    # success_url = reverse_lazy('home-page')
    template_name = 'posts/_modal_answer_edit.html'
    pk_url_kwarg = 'answer_id'

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            data = {'status': 'success'}
            return JsonResponse(data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditAnswer, self).get_context_data()
        context['modal_question'] = Question.objects.get(pk=self.object.question.pk)
        return context


# Create your views here.
class DeleteAnswerAjax(View):
    def post(self, request):
        if self.request.is_ajax():
            answer_id = request.POST['answer_id']
            user_id = self.request.user.pk
            data = {}
            try:
                answer = Answer.objects.get(id=answer_id, user_id=user_id)
                answer.delete()
                data['status'] = 'answerDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'

            return JsonResponse(data)


# Create your views here.
class UpvoteAnswerAjax(View):
    def post(self, request):
        # self.request == request -> request is an attribute and also a parameter, but why... hm ?
        if self.request.is_ajax():
            answer_id = request.POST['answer_id']
            user_id = request.POST['user_id']
            data = {}
            try:
                upvote = Upvotes.objects.get_or_create(answer_id=answer_id, user_id=user_id)
                # Means answer wasn't upvoted before
                if upvote[1]:
                    data['status'] = 'upvoteSaved'
                else:
                    # Delete if was already upvoted
                    upvote[0].delete()
                    data['status'] = 'upvoteDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'
            return JsonResponse(data)


class BookmarkAnswerAjax(View):
    def post(self, request):
        # self.request == request, they are attributes and also parameters
        if self.request.is_ajax():
            answer_id = request.POST['answer_id']
            user_id = request.POST['user_id']
            data = {}
            try:
                bookmark = Bookmarks.objects.get_or_create(bookmark_id=answer_id, user_id=user_id)
                # Means answer wasn't bookmarked before
                if bookmark[1]:
                    data['status'] = 'bookmarkSaved'
                else:
                    # Delete if was already bookmarked
                    bookmark[0].delete()
                    data['status'] = 'bookmarkDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'
            return JsonResponse(data)


class FollowQuestionAjax(View):
    def post(self, request):
        if self.request.is_ajax():
            question_id = request.POST['question_id']
            user_id = self.request.user.pk
            data = {}
            try:
                follow_question = FollowQuestion.objects.get_or_create(user_id=user_id, question_id=question_id)
                if follow_question[1]:
                    data['status'] = 'questionFollowed'
                else:
                    # Delete if was already bookmarked
                    follow_question[0].delete()
                    data['status'] = 'questionUnfollowed'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'
            return JsonResponse(data)


class RemindQuestionAjax(View):
    def post(self, request):
        if self.request.is_ajax():
            question_id = request.POST['question_id']
            user_id = self.request.user.pk
            data = {}
            try:
                follow_question = AnswerLater.objects.get_or_create(user_id=user_id, question_id=question_id)
                if follow_question[1]:
                    data['status'] = 'reminderCreated'
                else:
                    # Delete if was already bookmarked
                    follow_question[0].delete()
                    data['status'] = 'reminderDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'
            return JsonResponse(data)
