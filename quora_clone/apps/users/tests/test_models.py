from django.test import TestCase

from quora_clone.apps.users.models import User


class UserModelTests(TestCase):

    def setUp(self):
        self.user = User(username='TestUser')

    def test_string_representation(self):
        self.assertEqual(f'@{self.user.username}', str(self.user))

    def test_topic_get_absolute_url(self):
        self.assertEqual(f'/users/@{self.user.username}/profile/', self.user.get_absolute_url())
