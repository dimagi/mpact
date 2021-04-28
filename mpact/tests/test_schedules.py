from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from mpact.models import GroupChat, ScheduledMessage
from mpact.tests.util import run_test_schedule, TEST_GROUP_ID


class ScheduleTestCase(TestCase):

    def test_happy_upload(self):
        group = GroupChat.objects.create(id=TEST_GROUP_ID)
        result = run_test_schedule()['data']
        self.assertEqual([], result['bad titles'])
        self.assertEqual(6, ScheduledMessage.objects.count())
        self.assertEqual(6, ScheduledMessage.objects.filter(enabled=True).count())
        # spot check
        message = ScheduledMessage.objects.get(group=group, day=1)
        self.assertEqual('Hello world!', message.message)
        self.assertEqual('A comment', message.comment)
        message_2 = ScheduledMessage.objects.get(group=group, day=2)
        self.assertEqual('Hello again', message_2.message)
        self.assertEqual('A different comment', message_2.comment)

        # also rudimentarily check periodic task creation
        self.assertEqual(6, ClockedSchedule.objects.count())
        self.assertEqual(6, PeriodicTask.objects.count())
        self.assertEqual(6, PeriodicTask.objects.filter(enabled=True).count())

    def test_reschedule(self):
        group = GroupChat.objects.create(id=TEST_GROUP_ID)
        run_test_schedule()
        group.schedule_start_date = timezone.now().date() + timedelta(days=2)
        group.schedule_start_time = timezone.now().time()
        group.save()
        # do the schedule again, it should disable the previously created ones, and create
        # 6 more of everything
        run_test_schedule()
        self.assertEqual(12, ScheduledMessage.objects.count())
        self.assertEqual(6, ScheduledMessage.objects.filter(enabled=True).count())
        self.assertEqual(12, ClockedSchedule.objects.count())
        self.assertEqual(12, PeriodicTask.objects.count())
        self.assertEqual(6, PeriodicTask.objects.filter(enabled=True).count())

    def test_reschedule_in_past(self):
        group = GroupChat.objects.create(id=TEST_GROUP_ID)
        run_test_schedule()
        group.schedule_start_date = timezone.now().date() - timedelta(days=5)
        group.schedule_start_time = timezone.now().time()
        group.save()
        # do the schedule again, it should disable the previously created ones,
        # and only create the last two messages (which are scheduled > 5 days out)
        run_test_schedule()
        self.assertEqual(12, ScheduledMessage.objects.count())
        self.assertEqual(6, ScheduledMessage.objects.filter(enabled=True).count())
        self.assertEqual(8, ClockedSchedule.objects.count())
        self.assertEqual(8, PeriodicTask.objects.count())
        self.assertEqual(2, PeriodicTask.objects.filter(enabled=True).count())
