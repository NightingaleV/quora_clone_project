from urllib.request import urlopen
from tempfile import NamedTemporaryFile

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from django.db.models.signals import post_save


class User(AbstractUser):
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))

    description = models.TextField(max_length=75, blank=True)
    gender = models.CharField(max_length=8, default='Male', blank=False, choices=GENDER_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    follow_system = models.ManyToManyField('self', symmetrical=False, through='UserFollowersBridge')

    def __str__(self):
        return "@{}".format(self.username)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'alias': self.username})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @classmethod
    def save_default_image(cls, sender, instance, created, *args, **kwargs):
        if created:
            import random
            num = random.randint(1, 6)
            if instance.gender == 'male':
                instance.profile_image = 'profile_images/defaults/default_m_00{0}.jpg'.format(num)
            else:
                instance.profile_image = 'profile_images/defaults/default_f_00{0}.jpg'.format(num)
            instance.save()


# Django Db Signal - Observer Registration
post_save.connect(User.save_default_image, sender=User)


class UserFollowersBridge(models.Model):
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('followers', 'following')

    def __str__(self):
        return f'{self.follower} is following {self.following}'
