# Generated by Django 2.2 on 2021-03-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpact', '0009_auto_20210302_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChatUnread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('room_id', models.IntegerField()),
                ('unread_count', models.IntegerField(default=0)),
            ],
            options={
                'unique_together': {('user_id', 'room_id')},
            },
        ),
    ]