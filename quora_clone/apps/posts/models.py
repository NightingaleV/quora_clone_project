from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from quora_clone.config.settings.base import AUTH_USER_MODEL
from quora_clone.apps.utils.models import CreationModificationDateMixin
from quora_clone.apps.topics.models import Topic


# Create your models here.
class Question(CreationModificationDateMixin, models.Model):
    content = models.CharField(max_length=300, blank=False, unique=True)
    slug = models.SlugField(max_length=350, allow_unicode=True, unique=True)
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='questions', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.content}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.content)
        super(Question, self).save(*args, **kwargs)


class Answer(CreationModificationDateMixin, models.Model):
    content = models.TextField()
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    bookmarks = models.ManyToManyField(AUTH_USER_MODEL, through='Bookmarks', related_name='bookmarks')
    upvotes = models.ManyToManyField(AUTH_USER_MODEL, through='Upvotes', related_name='upvotes')

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

    def __str__(self):
        return f"{self.user} upvoted the {self.answer}"

    class Meta:
        unique_together = ['answer', 'user']
