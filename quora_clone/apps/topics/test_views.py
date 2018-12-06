from django.test import TestCase
from django.urls import resolve
from .views import ListTopic


class TopicViews(TestCase):
    def test_topic_url_resolves_to_topic_view(self):
        found = resolve('/topics/')
        self.assertEqual(found.func.view_class, ListTopic)

    def test_topic_list_template_implementation(self):
        request = HttpRequest()
        topic_list = ListTopic()
        response = topic_list.get(request=request)
        expected_html = render_to_string('topics/topics_list.html')
        self.assertEqual(response.content.decode(), expected_html)
