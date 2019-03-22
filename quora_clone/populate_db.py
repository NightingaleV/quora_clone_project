import os
import sys
import random
import pytz
import django
from django.contrib.auth import get_user_model
from faker import Faker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quora_clone.config.settings.local')
django.setup()

from quora_clone.apps.topics.models import Topic, TopicSubscription
from quora_clone.apps.posts.models import Question, Answer, Upvotes

TOPICS = ['Art','Food', 'Gaming','Health', 'History', 'Technology', 'Sports', 'Life', 'Finance', 'Design',
          'Humor', 'Entertainment', 'Marketing', 'Psychology', 'The Universe', 'Productivity',]


User = get_user_model()
fake = Faker()


def create_topic(topic):
    topic_object = Topic.objects.get_or_create(name=topic)[0]
    print(topic_object.name + ' was created')
    return topic_object


def create_question(user, topic):
    fake_question = fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)[:-1]
    fake_question += '?'

    question_object = Question.objects.get_or_create(content=fake_question, topic=topic, user=user)[0]
    return question_object


def create_answer(user, question):
    fake_answer = fake.text(max_nb_chars=500)
    answer_object = Answer.objects.get_or_create(content=fake_answer,
                                                 user=user,
                                                 question=question,
                                                 )[0]
    return answer_object


def create_user():
    gender = ['male', 'female']
    gender_pick = random.choice(gender)
    if gender_pick is 'male':
        fake_first_name = fake.first_name_male()
        fake_last_name = fake.last_name_male()
        fake_username = fake.user_name()
        fake_email = fake.free_email()

    else:
        fake_first_name = fake.first_name_female()
        fake_last_name = fake.last_name_female()
        fake_username = fake.user_name()
        fake_email = fake.free_email()

    user_object = User.objects.get_or_create(first_name=fake_first_name,
                                             last_name=fake_last_name,
                                             username=fake_username,
                                             email=fake_email,
                                             gender=gender_pick)[0]
    user_object.set_password('password')
    user_object.save()
    return user_object


def populate_database(n_user):
    n_topics_subscribed = random.randint(1, (len(TOPICS) - 1))
    user_objects, topics_objects, question_objects, answer_objects = [], [], [], []

    # Creating TOPICS
    for topic in TOPICS:
        topics_object = create_topic(topic)
        topics_objects.append(topics_object)

    # Creating USERS
    for i in range(n_user):
        user_object = create_user()
        user_objects.append(user_object)

    for user in user_objects:
        subscribed_topics = random.sample(topics_objects, n_topics_subscribed)
        print('Subscribing Topics')
        for topic in subscribed_topics:
            # User Subscribe Topic
            knowledge = random.randint(0, 10)
            interest = random.randint(0, 10)
            TopicSubscription.objects.get_or_create(user=user, topic=topic, interest=interest, knowledge=knowledge)

            # User ASK Questions in topic
            print('Asking Question')
            for _ in range(random.randint(0, 10)):
                question = create_question(user, topic)
                question_objects.append(question)

            # User ANSWER question in topic
            print('Anwering Question')
            questions_not_written_by_user = [question for question in question_objects if question.user is user]
            if len(questions_not_written_by_user) is 0:
                choose_n = 0
            else:
                choose_n = random.randint(0, len(questions_not_written_by_user) - 1)

            questions_to_answer = random.sample(questions_not_written_by_user, choose_n)
            for quest in questions_to_answer:
                answer = create_answer(user, quest)
                answer_objects.append(answer)

            # User UPVOTE answer in question
            print('Upvoting Answer')
            answers_not_written_by_user = [answer for answer in answer_objects if answer.user is user]
            if len(answers_not_written_by_user) is 0:
                choose_n = 0
            else:
                choose_n = choose_n = random.randint(0, len(answers_not_written_by_user) - 1)
            answers_to_upvote = random.sample(answers_not_written_by_user, choose_n)
            for answer in answers_to_upvote:
                Upvotes.objects.get_or_create(user=user, answer=answer)


def format_db():
    User.objects.all().delete()
    Topic.objects.all().delete()


if __name__ == '__main__':
    print('Formating the Database')
    format_db()
    print("Populating the Database...Please Wait")
    populate_database(30)
    print('Populating Complete')
