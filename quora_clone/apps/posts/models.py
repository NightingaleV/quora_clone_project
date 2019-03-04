from django.db import models
from django.utils.text import slugify

from quora_clone.config.settings.base import AUTH_USER_MODEL
from quora_clone.apps.utils.models import CreationModificationDateMixin
from quora_clone.apps.topics.models import Topic


# Create your models here.
class Question(CreationModificationDateMixin, models.Model):
    title = models.CharField(max_length=300, blank=False, unique=True)
    slug = models.SlugField(max_length=350, allow_unicode=True, unique=True)
    topic = models.ForeignKey(Topic, related_name='questions', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='asker', on_delete=models.CASCADE)

    class Meta:
        ordering = '-created_at'

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)
