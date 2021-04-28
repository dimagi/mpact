from django.test import TestCase
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from mpact.models import GroupChat, ScheduledMessage
from mpact.tests.util import run_test_schedule


class ScheduleTestCase(TestCase):
    GROUP_ID = '12345'

    def test_happy_upload(self):
        GroupChat.objects.create(id=self.GROUP_ID)
        result = run_test_schedule()['data']
        self.assertEqual([], result['bad titles'])
        self.assertEqual(6, ScheduledMessage.objects.count())
        self.assertEqual(6, ClockedSchedule.objects.count())
        self.assertEqual(6, PeriodicTask.objects.count())
