from django.test import TestCase

from quora_clone.apps.users.models import User


class UserModelTests(TestCase):

    def setUp(self):
        self.user = User(username='TestUser')

    def test_string_representation(self):
        self.assertEqual(str(self.user), f'@{self.user.username}')

    def test_topic_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), f'/users/{self.user.username}/')
