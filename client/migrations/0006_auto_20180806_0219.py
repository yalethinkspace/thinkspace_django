# Generated by Django 2.1 on 2018-08-06 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20180806_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='description',
        ),
        migrations.RemoveField(
            model_name='user',
            name='links',
        ),
        migrations.AddField(
            model_name='user',
            name='resume',
            field=models.URLField(blank=True),
        ),
    ]