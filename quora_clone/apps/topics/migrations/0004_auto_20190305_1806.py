# Generated by Django 2.1.7 on 2019-03-05 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20190303_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topicsubscription',
            old_name='knowlage',
            new_name='knowledge',
        ),
        migrations.AlterField(
            model_name='topicsubscription',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_by', to='topics.Topic'),
        ),
        migrations.AlterField(
            model_name='topicsubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]
