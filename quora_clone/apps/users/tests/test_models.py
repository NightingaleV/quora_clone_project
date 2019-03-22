from django.test import TestCase

from quora_clone.apps.users.models import User, UserFollowersBridge


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User(username='TestUser')

    def test_string_representation(self):
        self.assertEqual(str(self.user), f'@{self.user.username}')

    def test_topic_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), f'/users/@{self.user.username}/')


class TestUserFollowersBridge(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='TestUser1')
        self.user2 = User.objects.create(username='TestUser2')

    def test_str(self):
        object = UserFollowersBridge.objects.get_or_create(follower=self.user1, following=self.user2)[0]
        self.assertEqual('@TestUser1 is following @TestUser2', str(object))
