import json
import uuid
from datetime import timedelta
from dateutil.parser import parse
from django.utils import timezone
from django.utils.timezone import make_aware
from django_celery_beat.models import ClockedSchedule, PeriodicTask


def rebuild_schedule_for_group(group, messages=None):
    messages = messages or group.scheduled_messages.filter(enabled=True)
    disable_tasks_for_group(group)
    create_new_tasks_for_group(group, messages)


def disable_tasks_for_group(group):
    """
    Disables any scheduled message tasks associated with the group.
    """
    tasks = get_periodic_tasks_for_group(group)
    tasks.update(
        enabled=False,
    )


def create_new_tasks_for_group(group, messages):
    start_date_time = parse(f"{group.schedule_start_date} {group.schedule_start_time}")
    # silences timezone warnings, though we may need to be smarter in the future and allow
    # groups to set their own timezones
    start_date_time = make_aware(start_date_time)
    for message in messages:
        # only schedule things in the future otherwise past messages go out immediately
        message_time = start_date_time + timedelta(days=message.day)
        if message_time > timezone.now():
            schedule, __ = ClockedSchedule.objects.get_or_create(
                clocked_time=message_time,
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
