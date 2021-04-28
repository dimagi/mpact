import json

from django.test import TestCase

from mpact.models import GroupChat, ScheduledMessage
from mpact.scheduling import get_periodic_tasks_for_group, rebuild_schedule_for_group


class PeriodicTaskTestCase(TestCase):
    GROUP_1_ID = 12345
    GROUP_2_ID = 54321

    def test_query_by_group(self):
        g1 = GroupChat.objects.create(id=self.GROUP_1_ID)
        g2 = GroupChat.objects.create(id=self.GROUP_2_ID)
        # have to refresh from DB to get dates/times back properly
        g1.refresh_from_db()
        g2.refresh_from_db()
        for i in range(1, 5):
            ScheduledMessage.objects.create(
                group=g1,
                day=i,
                message=f'g1 m{i}'
            )
            ScheduledMessage.objects.create(
                group=g2,
                day=i,
                message=f'g2 m{i}'
            )
        rebuild_schedule_for_group(g1)
        rebuild_schedule_for_group(g2)

        g1_tasks = get_periodic_tasks_for_group(g1)
        self.assertEqual(4, len(g1_tasks))
        for i, task in enumerate(g1_tasks):
            args = json.loads(task.args)
            self.assertEqual(self.GROUP_1_ID, args[0])
            self.assertEqual(f'g1 m{i + 1}', args[1])

        g2_tasks = get_periodic_tasks_for_group(g2)
        self.assertEqual(4, len(g2_tasks))
        for i, task in enumerate(g2_tasks):
            args = json.loads(task.args)
            self.assertEqual(self.GROUP_2_ID, args[0])
            self.assertEqual(f'g2 m{i + 1}', args[1])
