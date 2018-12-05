from django.test import TestCase
from django.urls import resolve
import sys

from .models import Topic
from . import views


# Create your tests here.
class TopicTest(TestCase):
    def test_topic_url_resolves_to_topic_view(self):
        found = resolve('/topics/')
        # Why root module not included?
        print(found.func.view_class.__module__)
        self.assertEqual(found.func.view_class.__name__, views.ListTopic.__name__)

    def test_string_representation(self):
        topic = Topic(name='Default Topic')
        self.assertEqual(str(topic), '# {}'.format(topic.name))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Topic._meta.verbose_name_plural), "topics")

    # def test_topic_get_absolute_url(self):
    #     topic = Topic(name='Default Topic')
    #     self.assertEqual(topic.get_absolute_url(), f'/topic/{Topic.name}')

    # https: // test - driven - django - development.readthedocs.io / en / latest / 02 -
    # models.html  # creating-entries-from-the-admin-site
