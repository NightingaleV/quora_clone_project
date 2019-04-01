from django.test import TestCase, RequestFactory, Client
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
from quora_clone.apps.posts.models import Question, Answer, Upvotes, Bookmarks, AnswerLater
from quora_clone.apps.topics.models import Topic

User = get_user_model()


class TestAjax(TestCase):

    def setUp(self):
        self.client = Client()

        # Request keywords for ajax
        self.json_kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        # Prepare Data
        # User
        self.user = User.objects.get_or_create(username='test_user')[0]
        self.user.set_password('12345')
        self.user.save()

        # Topic
        self.topic = Topic.objects.get_or_create(name='Interesting Topic')[0]
        # Question
        self.question = Question.objects.get_or_create(topic=self.topic, content='Example Question', user=self.user)[0]
        # Answer
        self.answer = Answer.objects.get_or_create(question=self.question, user=self.user, content='Example Answer')[0]


class TestUpvoteAnswerAjax(TestAjax):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/upvote-answer/'
        self.url_name = 'posts:upvote-answer'

    def test_ajax_response(self):
        self.client.login(username='test_user', password='12345')

        # Send Upvote request
        json_data = {'user_id': self.user.id, 'answer_id': self.answer.pk}
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'upvoteSaved')

        # Send Downvote request
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'upvoteDeleted')


class TestBookmarkAnswerAjax(TestAjax):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/bookmark-answer/'
        self.url_name = 'posts:bookmark-answer'

    def test_ajax_response(self):
        self.client.login(username='test_user', password='12345')

        # Send Upvote request
        json_data = {'user_id': self.user.id, 'answer_id': self.answer.pk}
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'bookmarkSaved')

        # Send Downvote request
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'bookmarkDeleted')


class TestFollowQuestionAjax(TestAjax):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/follow-question/'
        self.url_name = 'posts:follow-question'

    def test_ajax_response(self):
        self.client.login(username='test_user', password='12345')

        # Send Upvote request
        json_data = {'user_id': self.user.id, 'question_id': self.question.pk}
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'questionFollowed')

        # Send Downvote request
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'questionUnfollowed')


class TestRemindQuestionAjax(TestAjax):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/remind-question/'
        self.url_name = 'posts:remind-question'

    def test_ajax_response(self):
        self.client.login(username='test_user', password='12345')

        # Send Upvote request
        json_data = {'user_id': self.user.id, 'question_id': self.question.pk}
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'reminderCreated')

        # Send Downvote request
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'reminderDeleted')
