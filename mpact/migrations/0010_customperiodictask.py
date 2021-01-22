# Generated by Django 2.2 on 2021-01-19 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0014_remove_clockedschedule_enabled'),
        ('mpact', '0009_individual_access_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPeriodicTask',
            fields=[
                ('periodictask_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_celery_beat.PeriodicTask')),
                ('message', models.TextField(blank=True, help_text='Message', verbose_name='Message')),
            ],
            bases=('django_celery_beat.periodictask',),
        ),
    ]
