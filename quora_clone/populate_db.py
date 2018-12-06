import os
import sys
import django
from django.contrib.auth import get_user_model
from faker import Faker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quora_clone.config.settings.local')
django.setup()
from quora_clone.apps.topics.models import Topic

TOPICS = ['Health', 'History', 'Technology', 'Sports', 'Life', 'Finance', 'Design',
          'Humor', 'Entertainment', 'Marketing', 'Psychology', 'The Universe', 'Cooking']

User = get_user_model()

fake = Faker()


def add_topic(topic):
    topic_object = Topic.objects.get_or_create(name=topic)[0]
    topic_object.save()
    print(topic_object.name + ' was created')
    return topic_object


def add_user(first_name, last_name, username, email):
    user_object = User.objects.get_or_create(first_name=first_name,
                                             last_name=last_name,
                                             username=username,
                                             email=email)[0]
    user_object.set_password('password')
    user_object.save()
    return user_object


def populate_database(n_user):
    topics_objects = []
    user_objects = []

    for topic in TOPICS:
        topics_object = add_topic(topic)
        topics_objects.append(topics_object)

    for _ in range(n_user):
        fake_first_name = fake.first_name()
        fake_last_name = fake.last_name()
        fake_username = fake.user_name()
        fake_email = fake.free_email()
        user_object = add_user(fake_first_name, fake_last_name, fake_username, fake_email)
        user_objects.append(user_object)


def format_db():
    User.objects.all().delete()
    Topic.objects.all().delete()


if __name__ == '__main__':
    print('Formating the Database')
    format_db()
    print("Populating the Database...Please Wait")
    populate_database(10)
    print('Populating Complete')
