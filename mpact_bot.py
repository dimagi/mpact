import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot.settings")
django.setup()

from channels.layers import get_channel_layer
from django.db.models import F
from telethon import TelegramClient, events
from telethon.tl import types

from mpact.models import (
    Bot,
    BotIndividual,
    Chat,
    ChatBot,
    Individual,
    User,
    UserChatUnread,
)
from mpact.serializers import ChatSerializer, MessageSerializer
from telegram_bot.constants import (
    BOT_TOKEN,
    FIRST_NAME,
    FROM_GROUP,
    LAST_NAME,
    MESSAGE,
    ROOM_ID,
    SENDER_ID,
    SENDER_NAME,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
    TELEGRAM_MSG_ID,
    USERNAME,
    WEBSOCKET_ROOM_NAME,
)
from telegram_bot.logger import logger
from telegram_bot.messages import WELCOME
from telegram_bot.utils import get_or_none, increment_messages_count

bot_client = TelegramClient("bot", TELEGRAM_API_ID, TELEGRAM_API_HASH).start(
    bot_token=BOT_TOKEN
)


@bot_client.on(events.ChatAction)
async def chat_handler(event):
    """
    Event handler for chat action such as chat created, user added, user joined and new title
    """
    try:
        if event.created:
            data = {
                "id": event.action_message.peer_id.chat_id,
                "title": event.new_title,
                "created_at": event.action_message.date,
                "participant_count": len(event.users),
            }
            serializer = ChatSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            # add newly created group details in the database
            chat = Chat.objects.create(**data)
            for user in event.action_message.action.users:
                user_details = await bot_client.get_entity(user)
                current_bot = await bot_client.get_me()

                if user_details.username == current_bot.username:
                    # add bot details in the database
                    bot, created = Bot.objects.get_or_create(
                        id=user_details.id,
                        defaults={
                            USERNAME: user_details.username,
                            FIRST_NAME: user_details.first_name,
                            LAST_NAME: user_details.last_name,
                        },
                    )
                    chat_bot = ChatBot.objects.create(chat=chat, bot=bot)
                    chat_bot.save()

            # creating records in the UserChatUnread model for maintaining
            # unread count for each user and group chat.
            for user in User.objects.all():
                UserChatUnread.objects.create(user_id=user.pk, room_id=data["id"])

        elif event.new_title:
            chat = get_or_none(Chat, id=event.action_message.peer_id.chat_id)
            if chat:
                chat.title = event.new_title
                chat.save()

        elif event.user_added or event.user_joined:
            increment_decrement_participant_count(event, "+")

        elif event.user_kicked or event.user_left:
            increment_decrement_participant_count(event, "-")

    except Exception as exception:
        logger.exception(exception)


def increment_decrement_participant_count(event, operator):
    chat = get_or_none(Chat, id=abs(event.chat_id))
    if chat:
        if operator == "+":
            chat.participant_count += len(event.users)
        elif operator == "-":
            chat.participant_count -= len(event.users)
        chat.save()


@bot_client.on(events.NewMessage(incoming=True))
async def incoming_message_handler(event):
    """
    Event handler for all the incoming messages
    """
    try:
        channel_layer = get_channel_layer()
        msg_data = message_data(
            event.chat_id,
            event.message.id,
            event.sender.id,
            event.sender.first_name,
            event.text,
        )

        # check if the message is from individual(PeerUser) or group(PeerChat) chat
        if isinstance(event.message.peer_id, types.PeerUser):
            msg_data[FROM_GROUP] = False
            if event.text == "/start":
                # creating records in the UserChatUnread model for maintaining
                # unread count for each user and individual chat.
                for user in User.objects.all():
                    UserChatUnread.objects.create(
                        user_id=user.pk, room_id=event.message.peer_id.user_id
                    )

            await save_send_message(msg_data, channel_layer)

            if event.text == "/start":
                await start_handler(event, channel_layer)

        elif isinstance(event.message.peer_id, types.PeerChat):
            msg_data[FROM_GROUP] = True
            await save_send_message(msg_data, channel_layer)

    except Exception as exception:
        logger.exception(exception)


async def start_handler(event, channel_layer):
    """
    Handler for "/start"
    """
    current_bot = await bot_client.get_me()
    user_details = await bot_client.get_entity(event.message.peer_id.user_id)

    bot = Bot.objects.get(id=current_bot.id)

    individual, i_created = Individual.objects.get_or_create(
        id=user_details.id,
        defaults={
            USERNAME: user_details.username,
            FIRST_NAME: user_details.first_name,
            LAST_NAME: user_details.last_name,
            "access_hash": user_details.access_hash,
        },
    )

    bot_individual, bi_created = BotIndividual.objects.get_or_create(
        bot=bot, individual=individual
    )
    if bi_created:
        bot_individual.save()

    await event.respond(WELCOME)
    msg_data = message_data(
        event.chat_id, event.message.id, current_bot.id, current_bot.first_name, WELCOME
    )
    msg_data[FROM_GROUP] = False
    await save_send_message(msg_data, channel_layer)


def message_data(room_id, telegram_msg_id, sender_id, sender_name, message):
    return {
        ROOM_ID: abs(room_id),
        TELEGRAM_MSG_ID: telegram_msg_id,
        SENDER_ID: sender_id,
        SENDER_NAME: sender_name,
        MESSAGE: message,
    }


async def save_send_message(msg_data, channel_layer):
    """Save the message to the database and
    send to the connected websockets client"""

    serializer = MessageSerializer(data=msg_data)
    if serializer.is_valid():
        serializer.save()
        increment_messages_count(serializer)
        # incrementing the unread count for all the admin users
        UserChatUnread.objects.filter(room_id=msg_data[ROOM_ID]).update(
            unread_count=F("unread_count") + 1
        )

        await channel_layer.group_send(
            WEBSOCKET_ROOM_NAME,
            {"type": "chat_message", MESSAGE: serializer.data},
        )


def main():
    """Start the bot."""
    with bot_client:
        bot_client.run_until_disconnected()


if __name__ == "__main__":
    main()
