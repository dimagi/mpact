from mpact.models import Individual, Chat


def get_chat_by_telegram_id(telegram_id):
    """
    Return either a Chat or an Individual object with the associated telegram ID.
    """
    try:
        return Chat.objects.get(id=telegram_id)
    except Chat.DoesNotExist:
        return Individual.objects.get(id=telegram_id)

