from django.test import TestCase, RequestFactory
from django.urls import resolve
from django.template.loader import render_to_string
from .views import ListTopic


def setup_view(view, request, *args, **kwargs):
    """
    Mimic ``as_view()``, but returns view instance.
    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.
    """

    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class TestTopicListView(TestCase):
    def test_topic_url_resolves_to_topic_view(self):
        found = resolve('/topics/')
        self.assertEqual(found.func.view_class, ListTopic)

    def test_topic_list_template_implementation(self):
        request = RequestFactory()
        v = setup_view(ListTopic(), request)
        response = v.get(request=request).render()
        expected_html = render_to_string('topics/topics_list.html')
        self.assertEqual(response.content.decode(), expected_html)
