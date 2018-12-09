from django.db import models
from quora_clone.config.settings.base import AUTH_USER_MODEL
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import QuerySet


# Topic Query Set
# ------------------------------------------------------------------------------
class TopicQuerySet(QuerySet):
    def related_questions(self):
        return self.filter()


# Topic Model
# ------------------------------------------------------------------------------
class Topic(models.Model):
    """ Group containing posts """
    name = models.CharField(max_length=75, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    subscribers = models.ManyToManyField(AUTH_USER_MODEL, through='TopicSubscription')

    object = TopicQuerySet.as_manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'# {self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('topics:topic-detail', kwargs={'topic-slug': self.name})


# Topic <-> User relationship
# ------------------------------------------------------------------------------
class TopicSubscription(models.Model):
    """ Bridge Table for Topics <-> User relationship """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('topic', 'user')

    def __str__(self):
        return f'{self.user} is subscribed to the {self.topic}'
