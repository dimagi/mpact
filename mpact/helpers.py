from mpact.models import Individual, GroupChat


def get_chat_by_telegram_id(telegram_id):
    """
    Return either a GroupChat or an Individual object with the associated telegram ID.
    """
    try:
        return GroupChat.objects.get(id=telegram_id)
    except GroupChat.DoesNotExist:
        return Individual.objects.get(id=telegram_id)

