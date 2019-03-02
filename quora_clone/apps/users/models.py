from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))

    description = models.TextField(max_length=75, blank=True)
    gender = models.CharField(max_length=8, default='Male', blank=False, choices=GENDER_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return "@{}".format(self.username)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})
