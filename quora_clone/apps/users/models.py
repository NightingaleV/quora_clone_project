from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    def __str__(self):
        return "@{}".format(self.username)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})
