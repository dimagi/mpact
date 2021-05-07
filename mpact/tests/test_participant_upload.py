from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from mpact.models import GroupChat, ScheduledMessage, IndividualChat
from mpact.participants import ParticipantInfo, import_participants
from mpact.tests.util import run_test_schedule, TEST_GROUP_ID


class ParticipantUploadTestCase(TestCase):

    def test_upload_partipcants(self):
        telegram_id = 12345
        study_id = 's12345'
        phone_number = 'p12345'
        individual = IndividualChat.objects.create(id=telegram_id)
        info = ParticipantInfo(study_id, phone_number)
        # todo: mock telegram API lookup here
        import_participants([info])
        individual.refresh_from_db()
        self.assertEqual(individual.study_id, study_id)
