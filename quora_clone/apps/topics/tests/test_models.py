from django.test import TestCase

from quora_clone.apps.topics.models import Topic
from quora_clone.apps.topics.models import TopicSubscription


class TopicModelTests(TestCase):

    def test_string_representation(self):
        topic = Topic(name='Default Topic')
        self.assertEqual('#{}'.format(topic.name), str(topic))

    def test_verbose_name_plural(self):
        self.assertEqual("topics", str(Topic._meta.verbose_name_plural))

    def test_topic_get_absolute_url(self):
        topic = Topic(name='Default')
        topic.save()
        self.assertEqual(f'/topics/{topic.slug}/', topic.get_absolute_url())
