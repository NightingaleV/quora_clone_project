from django.test import TestCase
from django.contrib.auth import get_user_model

from quora_clone.apps.topics.models import Topic
from quora_clone.apps.posts.models import Question, Answer, Bookmarks, Upvotes

User = get_user_model()


class QuestionModelTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.get_or_create(name='topic')[0]
        self.user = User.objects.get_or_create(username='user')

    def test_string_representation(self):
        question_content = 'This is it'
        question = Question.objects.get_or_create(content=question_content, topic=self.topic)[0]
        self.assertEqual(question_content, str(question))

    def test_get_absolute_url(self):
        pass


class AnswerModelTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.get_or_create(name='topic')[0]
        self.question = Question.objects.get_or_create(content='question', topic=self.topic)[0]
        self.author = User.objects.get_or_create(username='author')[0]

    def test_string_representation(self):
        answer = Answer.objects.get_or_create(content='answer', question=self.question, user=self.author)[0]
        self.assertEqual('answer', str(answer))


class BookmarksTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.get_or_create(name='topic')[0]
        self.question = Question.objects.get_or_create(content='question', topic=self.topic)[0]
        self.author = User.objects.get_or_create(username='author')[0]
        self.answer = Answer.objects.get_or_create(content='answer', question=self.question, user=self.author)[0]
        self.user = User.objects.get_or_create(username='user')[0]

    def test_string_representation(self):
        bookmark = Bookmarks.objects.get_or_create(user=self.user, bookmark=self.answer)[0]
        self.assertEqual(f'{self.user} save the {self.answer}', str(bookmark))


class UpvotesTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.get_or_create(name='topic')[0]
        self.question = Question.objects.get_or_create(content='question', topic=self.topic)[0]
        self.author = User.objects.get_or_create(username='author')[0]
        self.answer = Answer.objects.get_or_create(content='answer', question=self.question, user=self.author)[0]
        self.user = User.objects.get_or_create(username='user')[0]

    def test_string_representation(self):
        upvote = Upvotes.objects.get_or_create(user=self.user, answer=self.answer)[0]
        self.assertEqual(f"{self.user} upvoted the {self.answer}", str(upvote))
