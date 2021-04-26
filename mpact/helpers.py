from mpact.models import IndividualChat, GroupChat


def get_chat_by_telegram_id(telegram_id):
    """
    Return either a GroupChat or an IndividualChat object with the associated telegram ID.
    """
    try:
        return GroupChat.objects.get(id=telegram_id)
    except GroupChat.DoesNotExist:
        return IndividualChat.objects.get(id=telegram_id)
