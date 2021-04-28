import json
import uuid
from datetime import timedelta
from dateutil.parser import parse
from django_celery_beat.models import ClockedSchedule, PeriodicTask


def rebuild_schedule_for_group(group, messages=None):
    start_date_time = parse(f"{group.schedule_start_date} {group.schedule_start_time}")
    messages = messages or group.scheduled_messages.all()

    for message in messages:
        schedule, __ = ClockedSchedule.objects.get_or_create(
            clocked_time=start_date_time + timedelta(days=message.day),
        )
        PeriodicTask.objects.create(
            clocked=schedule,
            name=str(uuid.uuid4()),
            task="mpact.tasks.send_msgs",
            args=json.dumps([group.id, message.message]),
            one_off=True,
        )


def get_periodic_tasks_for_group(group):
    # the args column looks like this: [503371387, "Hello world!"]
    # so we query for it starting with a bracket and ending with a comma followed by a space and quote
    return PeriodicTask.objects.filter(
        args__contains=f'[{group.id}, "'
    ).order_by('clocked__clocked_time')
