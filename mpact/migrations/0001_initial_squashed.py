# Generated by Django 2.2.17 on 2021-01-28 20:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mpact.models


class Migration(migrations.Migration):

    replaces = [
        ('mpact', '0001_initial'),
        ('mpact', '0002_chatdata'),
        ('mpact', '0003_auto_20201221_0907'),
        ('mpact', '0004_auto_20201222_1644'),
        ('mpact', '0005_auto_20201224_0527'),
        ('mpact', '0006_auto_20201224_1453'),
        ('mpact', '0007_auto_20210105_0853'),
        ('mpact', '0008_message'),
        ('mpact', '0009_individual_access_hash'),
        ('mpact', '0010_customperiodictask'),
        ('mpact', '0011_auto_20210122_1530'),
        ('mpact', '0012_auto_20210124_0649'),
    ]

    initial = True

    dependencies = [
        ('django_celery_beat', '0014_remove_clockedschedule_enabled'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.TextField()),
                ('first_name', models.TextField()),
                ('last_name', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BotIndividual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bot_individuals', to='mpact.Bot')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomPeriodicTask',
            fields=[
                ('periodictask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_celery_beat.PeriodicTask')),
                ('message', models.TextField(blank=True, help_text='Enter the Message', verbose_name='Message')),
            ],
            bases=('django_celery_beat.periodictask',),
        ),
        migrations.CreateModel(
            name='FlaggedMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.IntegerField()),
                ('message_id', models.IntegerField()),
                ('first_name', models.TextField()),
                ('message', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.TextField(null=True)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField(null=True)),
                ('access_hash', models.TextField()),
                ('bots', models.ManyToManyField(through='mpact.BotIndividual', to='mpact.Bot')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Phone number is invalid.', regex='^\\+?1?\\d{9,15}$'), mpact.models.validate_phone])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.IntegerField()),
                ('message', models.TextField(null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mpact.Individual')),
            ],
        ),
        migrations.CreateModel(
            name='ChatBot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mpact.Bot')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mpact.Chat')),
            ],
        ),
        migrations.AddField(
            model_name='botindividual',
            name='individual',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mpact.Individual'),
        ),
        migrations.AddField(
            model_name='bot',
            name='chats',
            field=models.ManyToManyField(through='mpact.ChatBot', to='mpact.Chat'),
        ),
    ]
