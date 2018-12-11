from django.test import TestCase, RequestFactory, Client
from django.urls import resolve, reverse
from django.template.loader import render_to_string
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth import get_user_model
from quora_clone.apps.users.views import UserCreateView, UserRedirectView

User = get_user_model()


class TestUserCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_path = '/users/register/'
        self.url_name = 'users:registration'
        self.template = 'users/users_register.html'
        self.response = self.client.get(self.url_path)

    # Test URLs
    def test_users_list_url(self):
        self.assertEqual(reverse(self.url_name), self.url_path)
        self.assertEqual(resolve(self.url_path).view_name, self.url_name)

    # Test URL returning a expected view
    def test_users_url_resolves_to_topic_view(self):
        resolver = resolve(self.url_path)
        self.assertEqual(resolver.func.view_class, UserCreateView)

    # Test View Template Implementation
    def test_users_create_template_implementation(self):

        # If using the right template
        self.assertTemplateUsed(self.response, self.template)

        # If page loads with status 200
        self.assertEqual(self.response.status_code, 200, f'Problem with template {self.template}')


class TestUserRedirectView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_path = '/users/redirect/'
        self.url_name = 'users:redirect'
        self.request_factory = RequestFactory()
        self.response = self.client.get(self.url_path)

    # Test URLs
    def test_topic_list_url(self):
        self.assertEqual(reverse(self.url_name), self.url_path)
        self.assertEqual(resolve(self.url_path).view_name, self.url_name)

    # Test URL returning a expected view
    def test_topic_url_resolves_to_topic_view(self):
        resolver = resolve(self.url_path)
        self.assertEqual(resolver.func.view_class, UserRedirectView)

    # Test View Template Implementation
    def test_topic_list_template_implementation(self):
        view = UserRedirectView()
        request = self.request_factory.get('/fake-url')
        request.user = User
        view.request = request
        self.assertEqual(view.get_redirect_url(), '/')


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
