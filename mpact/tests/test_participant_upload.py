import asyncio
from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from mpact.models import IndividualChat
from mpact.participants import ParticipantInfo, import_participants


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

class ParticipantUploadTestCase(TestCase):

    @mock.patch('mpact.participants.get_telegram_id', new_callable=AsyncMock)
    def test_upload_partipcants(self, mock_get_telegram_id):
        telegram_id = 12345
        mock_get_telegram_id.return_value = telegram_id
        study_id = 's12345'
        phone_number = 'p12345'
        individual = IndividualChat.objects.create(id=telegram_id)
        info = ParticipantInfo(study_id, phone_number)
        results = asyncio.run(import_participants([info]))
        result = results[0]
        self.assertEqual(info, result.participant_info)
        self.assertEqual(True, result.successful)
        individual.refresh_from_db()
        self.assertEqual(individual.study_id, study_id)
