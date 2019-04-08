from django.test import TestCase
from django.utils.safestring import mark_safe
from django.template import Context, Template, RequestContext
from django.test.client import RequestFactory


class TestUrlAddParametersTag(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/answered-questions/?active=feed')

    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_url_add_parameters(self):
        context = Context()
        context['request'] = self.request

        string = '{% load posts_template_tags %}'
        string += '<a href="?{% url_add_param parameter=1 %}"></a>'

        expected = mark_safe('<a href="?active=feed&parameter=1"></a>')
        rendered = self.render_template(string, context)
        self.assertEqual(expected, rendered)
