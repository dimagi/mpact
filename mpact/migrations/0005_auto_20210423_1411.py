# Generated by Django 2.2.20 on 2021-04-23 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpact', '0004_auto_20210423_1408'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Chat',
            new_name='GroupChat',
        ),
    ]
