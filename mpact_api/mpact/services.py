import os

from django.urls import reverse

from telegram.ext import Updater

from .constants import BOT_TOKEN, ID, MESSAGE, REPLACE
from .models import UserChat, UserData
from .serializers import ChatDataSerializer, UserDataSerializer

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def set_webhook() -> bool:
    # TODO: we can move this to config file or keep this as a seperate script.
    local_url = 'http://localhost:8000' + reverse("listen_msg")
    webhook_url = os.environ.get('WEBHOOK_URL') or local_url
    success = updater.bot.setWebhook(webhook_url, allowed_updates=[MESSAGE])
    return success


def save_chatdata(chat_data, chat_instance=None):
    if chat_instance:
        # To update already existing record
        chat_serializer = ChatDataSerializer(chat_instance, data=chat_data)
    else:
        # To create a new record
        chat_serializer = ChatDataSerializer(data=chat_data)
    if chat_serializer.is_valid(raise_exception=True):
        chat_serializer.save()


def save_userdata(userdata):
    user_serializer = UserDataSerializer(data=userdata)
    if user_serializer.is_valid(raise_exception=True):
        user_data_rec = UserData.objects.create(**userdata)
        user_data_rec.save()
        return user_data_rec


def save_userchat(chat_data, user_data_inst):
    user_chat_record = UserChat.objects.create(
        chat_id=chat_data[ID], user=user_data_inst
    )
    user_chat_record.save()


def anonymize(dict_: dict) -> None:
    """
    Recursively anonymize values in ``dict_`` in place.
    """
    for key, value in dict_.items():
        if isinstance(value, dict):
            anonymize(value)
        elif isinstance(value, list) and all(isinstance(v, dict) for v in value):
            for v in value:
                anonymize(v)
        elif key in REPLACE:
            dict_[key] = REPLACE[key]
    return dict_
