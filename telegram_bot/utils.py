from mpact.models import Chat, Individual
from rest_framework import status

from telegram_bot.constants import (
    DATA,
    FAIL_MSG,
    FROM_GROUP,
    IS_SUCCESS,
    MESSAGE,
    ROOM_ID,
    STATUS,
)
from telegram_bot.logger import logger


def get_or_none(model, **kwargs):
    """
    Returns model object if exists else None
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def exception(function):
    async def wrapper(*args):
        try:
            func = await function(*args)
            return func
        except Exception as exception:
            logger.exception(exception)
            return {
                DATA: {MESSAGE: FAIL_MSG, IS_SUCCESS: False},
                STATUS: status.HTTP_400_BAD_REQUEST,
            }

    return wrapper


def increment_messages_count(serializer):
    if serializer.data[FROM_GROUP]:
        chat_inst = Chat.objects.get(id=serializer.data[ROOM_ID])
        chat_inst.messages_count += 1
        chat_inst.save()
    else:
        indi_inst = Individual.objects.get(id=serializer.data[ROOM_ID])
        indi_inst.messages_count += 1
        indi_inst.save()
