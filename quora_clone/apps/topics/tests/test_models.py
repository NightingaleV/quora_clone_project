from django.test import TestCase

from quora_clone.apps.topics.models import Topic
from quora_clone.apps.topics.models import TopicSubscription


class TestTopicModel(TestCase):

    def test_string_representation(self):
        topic = Topic(name='Default Topic')
        self.assertEqual(str(topic), '# {}'.format(topic.name))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Topic._meta.verbose_name_plural), "topics")

    # def test_topic_get_absolute_url(self):
    #     topic = Topic(name='Default Topic')
    #     self.assertEqual(topic.get_absolute_url(), f'/topics/{Topic.name}')
