# Generated by Django 2.2 on 2020-11-12 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mpact', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userchat',
            old_name='user_id',
            new_name='user',
        ),
    ]