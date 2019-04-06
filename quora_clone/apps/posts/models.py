from django.db import models
from django.db.models import Q, FilteredRelation, Count
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q, Prefetch, Sum, Max

from quora_clone.config.settings.base import AUTH_USER_MODEL
from quora_clone.apps.utils.models import CreationModificationDateMixin
from quora_clone.apps.topics.models import Topic


# QUESTION
# ------------------------------------------------------------------------------
class QuestionQuerySet(models.QuerySet):

    def count_answers(self):
        return self.annotate(num_answers=Count('answers', True, filter=Q(answers__is_published=True)))

    def add_chance_user_to_answer(self, user):
        return self.annotate(num_knowlage=Max('topic__subscribed_by__knowledge',
                                              filter=Q(topic__subscribed_by__user=user)))

    def order_by_chance_to_answer(self):
        return self.order_by('-num_knowlage')

    def add_chance_to_like_a_answer(self, user):
        return self.annotate(num_interest=Max('topic__subscribed_by__interest',
                                              filter=Q(topic__subscribed_by__user=user)))

    def order_by_chance_to_like_a_answer(self):
        return self.order_by('-num_interest')

    def exclude_already_answered_by_user(self, user_id):
        return self.exclude(answers__user=user_id)

    def prefetch_followers_reminders(self):
        return self.prefetch_related('follow_question', 'reminder')

    def get_unanswered(self):
        return self.count_answers().filter(num_answers__lt=3)

    def prefetch_best_answers(self):
        answers_with_related_data = Answer.data.published().distinct().add_upvote_counter().order_by_upvotes().include_upvotes_bookmarks()
        return self.prefetch_related(Prefetch('answers', queryset=answers_with_related_data))

    def prefetch_bookmarks(self, user):
        answers_marked_as_bookmark = Answer.data.filter(saved_by__user=user).include_upvotes_bookmarks()
        return self.prefetch_related(Prefetch('answers', queryset=answers_marked_as_bookmark))


# Create your models here.
class Question(CreationModificationDateMixin, models.Model):
    content = models.CharField(max_length=300, blank=False, unique=True)
    slug = models.SlugField(max_length=350, allow_unicode=True, unique=True)
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='questions', on_delete=models.SET_NULL, null=True)
    reminder = models.ManyToManyField(AUTH_USER_MODEL, through='AnswerLater', related_name='reminder')
    follow_question = models.ManyToManyField(AUTH_USER_MODEL, through='FollowQuestion', related_name='follow_question')

    # Managers
    objects = models.Manager()
    data = QuestionQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.content}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.content)
        super(Question, self).save(*args, **kwargs)


# ANSWER
# ------------------------------------------------------------------------------
class AnswerQuerySet(models.QuerySet):
    def include_upvotes_bookmarks(self):
        return self.select_related('user').prefetch_related('upvotes', 'bookmarks')

    def add_upvote_counter(self):
        return self.annotate(num_upvotes=models.Count('upvotes'))

    def order_by_upvotes(self):
        return self.add_upvote_counter().order_by('-num_upvotes')

    def published(self):
        return self.filter(is_published=True)

    def unpublished(self):
        return self.filter(is_published=False)


class Answer(CreationModificationDateMixin, models.Model):
    content = models.TextField()
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    bookmarks = models.ManyToManyField(AUTH_USER_MODEL, through='Bookmarks', related_name='bookmarks')
    upvotes = models.ManyToManyField(AUTH_USER_MODEL, through='Upvotes', related_name='upvotes')
    is_published = models.BooleanField('is_published', default=True)

    objects = models.Manager()
    data = AnswerQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at']
        unique_together = ['id', 'user', 'question']

    def __str__(self):
        return f'{self.content}'


class Bookmarks(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='saved', on_delete=models.CASCADE)
    bookmark = models.ForeignKey(Answer, related_name='saved_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('creation date and time'), auto_now_add=True)

    def __str__(self):
        return f"{self.user} save the {self.bookmark}"

    class Meta:
        unique_together = ['bookmark', 'user']


class Upvotes(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='upvoted', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='upvoted_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('creation date and time'), auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.user} upvoted the {self.answer}"

    class Meta:
        unique_together = ['answer', 'user']


class FollowQuestion(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='follow_q', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='followed_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('creation date and time'), auto_now_add=True)

    def __str__(self):
        return f'{self.user} follow the {self.question}'

    class Meta:
        unique_together = ['user', 'question']


class AnswerLater(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='want_to_remind', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='to_be_reminded', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} follow the {self.question}'

    class Meta:
        unique_together = ['user', 'question']
