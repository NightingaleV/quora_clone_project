from django.core import mail
from django.test import TestCase, RequestFactory, Client
from quora_clone.apps.users.forms import UserCreationForm, UserUpdateForm


class TestUserCreationForm(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'johndoe23',
            'email': 'johndoe@gmail.com',
            'gender': 'male',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'battlefield1',
            'password2': 'battlefield1',
        }

    def test_clean_username(self):
        form = UserCreationForm(
            self.user_data
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(self.user_data['username'], form.clean_username())

        form.save()

        # This user already exist so cannot be created again
        form = UserCreationForm(
            self.user_data
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('username', form.errors)


class TestUserUpdateForm(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'johndoe23',
            'email': 'johndoe@gmail.com',
            'gender': 'male',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'battlefield1',
            'password2': 'battlefield1',
        }

    def test_form_valid(self):
        form = UserUpdateForm({
            'first_name': self.user_data['first_name'],
            'last_name': self.user_data['last_name'],
            'gender': self.user_data['gender'],
        })
        self.assertTrue(form.is_valid())



class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
                       'from@example.com', ['to@example.com'],
                       fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
