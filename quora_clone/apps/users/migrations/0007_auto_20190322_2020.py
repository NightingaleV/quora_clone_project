# Generated by Django 2.1.7 on 2019-03-22 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190307_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfollowersbridge',
            name='follower',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='userfollowersbridge',
            unique_together={('follower', 'following')},
        ),
    ]
