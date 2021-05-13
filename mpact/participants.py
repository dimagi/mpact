import json
from collections import namedtuple

import tablib

from mpact.exceptions import TelegramIdNotFound
from mpact.models import IndividualChat
from mpact.services import get_telegram_id

ParticipantInfo = namedtuple('ParticipantInfo', ['study_id', 'phone_number'])
ParticipantImportResult = namedtuple('ParticipantImportResult', ['participant_info', 'successful', 'message'])


def excel_to_participants(participant_excel):
    book = tablib.Databook()
    book.load(participant_excel, "xlsx")
    sheets = json.loads(book.export("json"))
    sheet = sheets[0]
    participants = []
    for n, row in enumerate(sheet["data"], start=1):
        participants.append(ParticipantInfo(row['Study ID'], str(row['Phone Number'])))

    return participants


async def import_participants(participants, user_mode=False):
    results = []
    for participant in participants:
        try:
            telegram_id = await get_telegram_id(participant.phone_number, user_mode)
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
