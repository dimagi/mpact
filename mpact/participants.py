from collections import namedtuple


ParticipantInfo = namedtuple('ParticipantInfo', ['study_id', 'phone_number'])


def import_participants(participants):
    for participant in participants:
        print(participant)

