import os
from django.test import TestCase
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from mpact.models import GroupChat, ScheduledMessage
from mpact.services import schedule_messages


class ScheduleTestCase(TestCase):
    GROUP_ID = '12345'

    def test_happy_upload(self):
        GroupChat.objects.create(id=self.GROUP_ID)
        schedule_file = os.path.join(os.path.dirname(__file__), 'data', 'test_schedules.xlsx')
        with open(schedule_file, 'rb') as f:
            result = schedule_messages(f)['data']

        self.assertEqual([], result['bad titles'])
        self.assertEqual(6, ScheduledMessage.objects.count())
        self.assertEqual(6, ClockedSchedule.objects.count())
        self.assertEqual(6, PeriodicTask.objects.count())
