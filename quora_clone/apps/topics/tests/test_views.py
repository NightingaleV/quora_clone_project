from django.test import TestCase, RequestFactory, Client
from django.urls import resolve, reverse
from django.template.loader import render_to_string
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth import get_user_model
from quora_clone.apps.topics.views import ListTopic

User = get_user_model()


class TestTopicListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_path = '/topics/'
        self.url_name = 'topics:list'
        self.template = 'topics/topics_list.html'
        self.context_keys = ['topics']
        self.response = self.client.get(self.url_path)

    # Test URLs
    def test_topic_list_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    # Test URL returning a expected view
    def test_topic_url_resolves_to_topic_view(self):
        resolver = resolve(self.url_path)
        self.assertEqual(ListTopic, resolver.func.view_class)

    # Test View Template Implementation
    def test_topic_list_template_implementation(self):
        # If using the right template
        self.assertTemplateUsed(self.response, self.template)

        # If return correct template content
        expected_html = render_to_string(self.template)
        self.assertHTMLEqual(expected_html, self.response.content.decode())

        # If page loads with status 200
        self.assertEqual(200, self.response.status_code, f'Problem with template {self.template}')

    # Test Return 200 for logged user
    def test_templates_for_user(self):
        user = User.objects.create(username='test_user')
        user.set_password('12345')
        user.save()

        self.client.login(username='test_user', password='12345')
        self.assertEqual(200, self.response.status_code, f'Problem with template {self.template}')

    # Test View Context Object
    def test_topic_list_view_context(self):
        for key in self.context_keys:
            self.assertTrue(f'Key {key} not in the context object', key in self.response.context)


# url = reverse('archive', args=[1988])
# assertEqual(url, '/archive/1988/')

# class DjangoRestFrameworkTests(TestCase):
#     def setUp(self):
#         Flavor.objects.get_or_create(title="title1", slug="slug1")
#         Flavor.objects.get_or_create(title="title2", slug="slug2")
#         self.create_read_url = reverse("flavor_rest_api")
#         self.read_update_delete_url = \
#         reverse("flavor_rest_api", kwargs={"slug": "slug1"})
#
#     def test_list(self):
#         response = self.client.get(self.create_read_url)
#         # Are both titles in the content?
#         self.assertContains(response, "title1")
#         self.assertContains(response, "title2")
#
#
#     def test_detail(self):
#         response = self.client.get(self.read_update_delete_url)
#         data = json.loads(response.content)
#         content = {"id": 1, "title": "title1", "slug": "slug1",
#                    "scoops_remaining": 0}
#         self.assertEquals(data, content)
#
#     def test_create(self):
#         post = {"title": "title3", "slug": "slug3"}
#         response = self.client.post(self.create_read_url, post)
#         data = json.loads(response.content)
#         self.assertEquals(response.status_code, 201)
#         content = {"id": 3, "title": "title3", "slug": "slug3",
#                    "scoops_remaining": 0}
#         self.assertEquals(data, content)
