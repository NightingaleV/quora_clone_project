from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from django.views import generic

from .models import Topic
from .views import ListTopic


# Create your tests here.
class TopicTest(TestCase):
    def test_topic_url_resolves_to_topic_view(self):
        found = resolve('/topics/')
        self.assertEqual(found.func.view_class, ListTopic)

    # def test_topic_list_template_implementation(self):
    #     request = HttpRequest()
    #     topic_list = ListTopic()
    #     response = topic_list.get(request=request)
    #     expected_html = render_to_string('topics/topics_list.html')
    #     self.assertEqual(response.content.decode(), expected_html)

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
