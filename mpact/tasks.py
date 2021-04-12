from celery import shared_task
from channels.layers import get_channel_layer
from django.db.models import F

from mpact.helpers import get_chat_by_telegram_id
from telegram_bot.constants import (
    DATA,
    FROM_GROUP,
    IS_SUCCESS,
    MESSAGE,
    MESSAGE_SENT,
    ROOM_ID,
    SENDER_ID,
    SENDER_NAME,
    TELEGRAM_MSG_ID,
    WEBSOCKET_ROOM_NAME,
)
from telegram_bot.utils import increment_messages_count
from telethon.tl.types import InputPeerChat, InputPeerUser

from .models import Chat, Individual, UserChatUnread
from .serializers import MessageSerializer
from .services import start_bot_client
from .views import new_or_current_event_loop


@shared_task
def send_msgs(receiver_id, message):
    return new_or_current_event_loop().run_until_complete(
        send_msg_task(receiver_id, message)
    )


async def send_msg_task(receiver_id, message):
    """
    Sends the message to the particular chat
    """
    async with start_bot_client() as bot:
        current_bot = await bot.get_me()
        room_id = int(receiver_id)
        chat_or_group = get_chat_by_telegram_id(receiver_id)
        group_mode = isinstance(chat_or_group, Chat)
        if group_mode:
            receiver = InputPeerChat(room_id)
        else:
            access_hash = chat_or_group.access_hash
            receiver = InputPeerUser(room_id, int(access_hash))

        msg_inst = await bot.send_message(receiver, message)
        message_data = {
            SENDER_ID: current_bot.id,
            SENDER_NAME: current_bot.first_name,
            ROOM_ID: int(receiver_id),
            MESSAGE: message,
            FROM_GROUP: group_mode,
            TELEGRAM_MSG_ID: msg_inst.id
        }
        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            serializer.save()
            increment_messages_count(serializer)
            # incrementing the unread count for all the admin users
            UserChatUnread.objects.filter(room_id=message_data[ROOM_ID]).update(
                unread_count=F("unread_count") + 1
            )
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                WEBSOCKET_ROOM_NAME, {"type": "chat_message", MESSAGE: serializer.data}
            )

    return {
        DATA: {MESSAGE: MESSAGE_SENT},
        IS_SUCCESS: True,
    }
