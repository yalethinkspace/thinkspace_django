# Generated by Django 2.1 on 2018-08-06 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0014_auto_20180806_2220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['timestamp']},
        ),
    ]
