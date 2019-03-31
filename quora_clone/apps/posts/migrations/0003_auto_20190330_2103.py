# Generated by Django 2.1.7 on 2019-03-30 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_auto_20190307_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerLater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_be_reminded', to='posts.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='want_to_remind', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='posts.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_q', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='follow_question',
            field=models.ManyToManyField(related_name='follow_question', through='posts.FollowQuestion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='reminder',
            field=models.ManyToManyField(related_name='reminder', through='posts.AnswerLater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='followquestion',
            unique_together={('user', 'question')},
        ),
        migrations.AlterUniqueTogether(
            name='answerlater',
            unique_together={('user', 'question')},
        ),
    ]
