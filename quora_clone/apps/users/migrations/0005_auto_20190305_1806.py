# Generated by Django 2.1.7 on 2019-03-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190303_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=8),
        ),
    ]
