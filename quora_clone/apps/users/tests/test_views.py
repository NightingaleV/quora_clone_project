from django.test import TestCase, RequestFactory, Client
from django.urls import resolve, reverse
from django.template.loader import render_to_string
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth import get_user_model
from quora_clone.apps.users.models import UserFollowersBridge
from quora_clone.apps.users.views import UserCreateView, UserRedirectView, UserUpdateView

User = get_user_model()


class TestUserCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.url_path = ''
        self.url_name = ''
        self.template = ''
        self.response = self.client.get(self.url_path)
        self.user_data = {
            'username': 'johndoe23',
            'email': 'johndoe@gmail.com',
            'gender': 'male',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': '123456Protos',
            'password2': '123456Protos'
        }

        # For ajax requests
        self.json_kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}


class TestUserCreateView(TestUserCase):
    def setUp(self):
        super().setUp()
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

    def test_get_success_url(self):
        response = self.client.post(self.url_path, self.user_data)
        self.assertRedirects(response, reverse('users:profile', kwargs={'alias': 'johndoe23'}), 302, 200)

    def test_create_user_by_request(self):
        response = self.client.post(self.url_path, self.user_data)
        self.assertEqual(User.objects.all().count(), 1)


class TestUpdateView(TestUserCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/users/edit/'
        self.url_name = 'users:profile-edit'
        self.user = User.objects.get_or_create(username=self.user_data['username'],
                                               email=self.user_data['email'],
                                               gender=self.user_data['gender'],
                                               first_name=self.user_data['first_name'],
                                               last_name=self.user_data['last_name'])[0]
        self.user.set_password(self.user_data['password1'])
        self.user.save()

    def test_form_valid(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password1'])
        self.new_data = {
            'description': '',
            'profile_image': '',
            'gender': 'male',
            'first_name': 'Krusty',
            'last_name': 'Doe',
        }
        self.user_data['first_name'] = 'Krusty'
        response = self.client.post(self.url_path, self.new_data)
        user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(user.first_name, 'Krusty')
        # self.assertEqual(reverse('users:profile-edit'), '/')


class TestUserRedirectView(TestUserCase):
    def setUp(self):
        self.url_path = '/users/redirect/'
        self.url_name = 'users:redirect'
        self.factory = RequestFactory()
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
        request = self.factory.get('/fake-url')
        request.user = User
        view.request = request
        self.assertEqual(view.get_redirect_url(), '/')


class TestUserFollowAjax(TestUserCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/users/follow/'
        self.url_name = 'users:follow'
        self.user = User.objects.get_or_create(username=self.user_data['username'],
                                               email=self.user_data['email'],
                                               gender=self.user_data['gender'],
                                               first_name=self.user_data['first_name'],
                                               last_name=self.user_data['last_name'])[0]
        self.user.set_password(self.user_data['password1'])
        self.user.save()

        self.user2 = User.objects.get_or_create(username='username2',
                                                email='email2',
                                                gender='male',
                                                first_name='first_name2',
                                                last_name='last_name2')[0]
        self.user2.set_password('password2')
        self.user2.save()

    def test_urls_for_view(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_login_required_mixin(self):
        json_data = {'following_id': self.user2.pk}
        response = self.client.post(reverse(self.url_name), data=json_data, **self.json_kwargs)
        self.assertRedirects(response, '/users/login/?next=' + self.url_path)

    def test_user_follow_user_correct_response(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password1'])
        # Id of user to follow
        json_data = {'following_id': self.user2.pk}
        response = self.client.post(reverse(self.url_name), data=json_data, **self.json_kwargs)

        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'followingCreated')
        # Check if follow relationship is created
        follow = UserFollowersBridge.objects.get(follower_id=self.user.pk, following_id=json_data['following_id'])
        self.assertEqual(follow.following_id, json_data['following_id'])

        # Second Request for deleting item
        response = self.client.post(reverse(self.url_name), data=json_data, **self.json_kwargs)
        data = response.json()
        self.assertEqual(data['status'], 'followingDeleted')
