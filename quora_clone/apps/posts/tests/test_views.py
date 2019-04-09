from django.test import TestCase, RequestFactory, Client
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
from quora_clone.apps.posts.models import Question, Answer, Upvotes, Bookmarks, AnswerLater
from quora_clone.apps.topics.models import Topic

User = get_user_model()


class PostsTestCase(TestCase):

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
        self.topic = Topic.objects.get_or_create(name='Example Topic')[0]
        # Question
        self.question = Question.objects.get_or_create(topic=self.topic, content='Example Question', user=self.user)[0]
        # Answer
        self.answer = Answer.objects.get_or_create(question=self.question, user=self.user, content='Example Answer')[0]


class CreateAnswerView(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/create-answer/'
        self.url_name = 'posts_ajax:create-answer'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_permissions(self):
        response = self.client.get(self.url_path)
        self.assertEqual(response.status_code, 403)

    def test_ajax_get_modal_response(self):
        self.client.login(username='test_user', password='12345')

        json_data = {
            'question_id': self.question.id,
        }
        response = self.client.get(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        self.assertIsNotNone(response.context['modal_question'])
        self.assertEqual(response.status_code, 200)

    def test_ajax_post_form_response(self):
        self.client.login(username='test_user', password='12345')

        form_data = {
            'question': self.question.id,
            'content': 'example question',
            'is_published': True
        }
        response = self.client.post(self.url_path, data=form_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'success')

    def test_nonajax_form_response(self):
        self.client.login(username='test_user', password='12345')
        json_data = {
            'question': self.question.id,
            'content': 'example question',
            'is_published': True
        }
        response = self.client.post(self.url_path, data=json_data)
        # Check if redirecting to question of that answer
        self.assertEqual(response.status_code, 302)


class EditAnswerView(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/edit-answer/'
        self.url_name = 'posts_ajax:edit-answer'

    def test_view_url(self):
        self.assertEqual(self.url_path + str(self.answer.id),
                         reverse(self.url_name, kwargs={'answer_id': self.answer.id}))
        # self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_ajax_get_modal_response(self):
        self.client.login(username='test_user', password='12345')

        json_data = {
            'question_id': self.question.id,
        }
        url = reverse(self.url_name, kwargs={'answer_id': self.answer.id})
        response = self.client.get(url, data=json_data, **self.json_kwargs)
        # Check if returning right response
        self.assertIsNotNone(response.context['modal_question'])
        self.assertEqual(response.status_code, 200)

    def test_ajax_post_form_response(self):
        self.client.login(username='test_user', password='12345')

        json_data = {
            'content': 'example question',
            'is_published': True
        }
        url = reverse(self.url_name, kwargs={'answer_id': self.answer.id})
        response = self.client.post(url, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'success')

    def test_permissions(self):
        response = self.client.get(reverse(self.url_name, kwargs={'answer_id': self.answer.id}))
        self.assertEqual(response.status_code, 403)

    def test_nonajax_form_response(self):
        self.client.login(username='test_user', password='12345')
        json_data = {
            'content': 'example question',
            'is_published': True
        }
        url = reverse(self.url_name, kwargs={'answer_id': self.answer.id})
        response = self.client.post(url, data=json_data)
        # Check if redirecting to question of that answer
        self.assertEqual(response.status_code, 302)


class DeleteAnswerAjax(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/delete-answer/'
        self.url_name = 'posts_ajax:delete-answer'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_ajax_response(self):
        self.client.login(username='test_user', password='12345')

        # Send Upvote request
        json_data = {'answer_id': self.answer.pk}
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'answerDeleted')


class PostsTestUpvoteAnswerCase(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/upvote-answer/'
        self.url_name = 'posts_ajax:upvote-answer'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_ajax_response(self):
        self.client.login(username='test_user', password='12345')

        # Send Upvote request
        json_data = {'answer_id': self.answer.pk}
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'upvoteSaved')

        # Send Downvote request
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'upvoteDeleted')


class PostsTestBookmarkAnswerCase(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/bookmark-answer/'
        self.url_name = 'posts_ajax:bookmark-answer'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_ajax_response(self):
        self.client.login(username='test_user', password='12345')

        # Send Upvote request
        json_data = {'answer_id': self.answer.pk}
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'bookmarkSaved')

        # Send Downvote request
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'bookmarkDeleted')


# QUESTION
# ------------------------------------------------------------------------------
class CreateQuestionView(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/create-question/'
        self.url_name = 'posts_ajax:create-question'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_permissions(self):
        response = self.client.get(self.url_path)
        self.assertEqual(response.status_code, 403)

    def test_ajax_get_modal_response(self):
        self.client.login(username='test_user', password='12345')

        json_data = {}
        response = self.client.get(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        self.assertEqual(response.status_code, 200)

    def test_ajax_post_form_response(self):
        self.client.login(username='test_user', password='12345')

        json_data = {
            'content': 'example_question',
            'topic': self.topic.id
        }
        response = self.client.post(self.url_path, data=json_data, **self.json_kwargs)
        # Check if returning right response
        data = response.json()
        self.assertEqual(data['status'], 'success')

    def test_nonajax_form_response(self):
        self.client.login(username='test_user', password='12345')
        json_data = {
            'content': 'example_question',
            'topic': self.topic.id
        }
        response = self.client.post(self.url_path, data=json_data)
        # Check if redirecting to question of that answer
        self.assertEqual(response.status_code, 302)


class TestFeedAnsweredQuestions(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.url_path = '/answered-questions/'
        self.url_name = 'answered-questions-list'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_login_required_mixin(self):
        response = self.client.get(reverse(self.url_name))
        self.assertRedirects(response, '/users/login/?next=' + self.url_path)

    def test_querysets(self):
        self.client.login(username='test_user', password='12345')
        possible_get_parameters = ['feed', 'following_questions', 'fav_writers', 'bookmarks', 'upvoted']

        for parameter in possible_get_parameters:
            response = self.client.get(f'{self.url_path}?active={parameter}')
            self.assertIsNotNone(response.context['questions_list'])
            self.assertEqual(response.status_code, 200)
        # print('Number of items: ' + str(len(response.context['questions_list'])))


class TestFeedUnansweredQuestions(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.url_path = '/unanswered-questions/'
        self.url_name = 'unanswered-questions-list'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

    def test_querysets(self):
        self.client.login(username='test_user', password='12345')
        possible_get_parameters = ['to_answer', 'reminder', 'my_concepts', 'my_answers', 'upvoted']

        for parameter in possible_get_parameters:
            response = self.client.get(f'{self.url_path}?active={parameter}')
            self.assertIsNotNone(response.context['questions_list'])
            self.assertEqual(response.status_code, 200)
        # print('Number of items: ' + str(len(response.context['questions_list'])))


class TestDetailPostsView(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_name = 'topics:posts:question-detail'

    def test_context_data(self):
        self.client.login(username='test_user', password='12345')
        response = self.client.get(
            reverse(self.url_name, kwargs={'topic_slug': self.topic.slug, 'question_slug': self.question.slug}))
        self.assertIsNotNone(response.context['answers_list'])
        self.assertIsNotNone(response.context['user_following'])


class QuestionTestFollowPostsCase(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/follow-question/'
        self.url_name = 'posts_ajax:follow-question'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

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


class QuestionTestRemindPostsCase(PostsTestCase):
    def setUp(self):
        super().setUp()
        self.url_path = '/actions/remind-question/'
        self.url_name = 'posts_ajax:remind-question'

    def test_view_url(self):
        self.assertEqual(self.url_path, reverse(self.url_name))
        self.assertEqual(self.url_name, resolve(self.url_path).view_name)

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
