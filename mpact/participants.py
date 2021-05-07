from collections import namedtuple

from mpact.exceptions import TelegramIdNotFound
from mpact.models import IndividualChat
from mpact.services import get_telegram_id

ParticipantInfo = namedtuple('ParticipantInfo', ['study_id', 'phone_number'])
ParticipantImportResult = namedtuple('ParticipantImportResult', ['participant_info', 'successful', 'message'])


async def import_participants(participants):
    results = []
    for participant in participants:
        try:
            telegram_id = await get_telegram_id(participant.phone_number)
            try:
                individual = IndividualChat.objects.get(id=telegram_id)
                individual.study_id = participant.study_id
                individual.save()
                results.append(
                    ParticipantImportResult(participant, True, '')
                )
            except IndividualChat.DoesNotExist:
                results.append(
                    ParticipantImportResult(participant, False, f'No participant with telegram ID {telegram_id} found')
                )
        except TelegramIdNotFound:
            results.append(
                ParticipantImportResult(participant, False, f'No Telegram user with phone number {participant.phone_number} found.')
            )
        except Exception as e:
            results.append(
                ParticipantImportResult(participant, False, f'Unknown error: {e}')
            )
    return results
