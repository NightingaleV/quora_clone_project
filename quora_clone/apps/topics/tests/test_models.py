from django.test import TestCase
from django.contrib.auth import get_user_model
from quora_clone.apps.topics.models import Topic
from quora_clone.apps.topics.models import TopicSubscription

User = get_user_model()


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


class TopicSubscriptionTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.get_or_create(name='Topic')[0]
        self.user = User.objects.get_or_create(username='user')[0]
        self.subscription = TopicSubscription.objects.get_or_create(user=self.user, topic=self.topic)[0]

    def test_string_representation(self):
        self.assertEqual('{} is subscribed to the {}'.format(self.user, self.topic), str(self.subscription))
