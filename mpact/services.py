import json
import re
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import timedelta

import tablib
from channels.layers import get_channel_layer
from dateutil.parser import parse
from django.db.models import F
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework import status
from telethon import TelegramClient
from telethon.errors import MessageIdInvalidError
from telethon.tl.types import InputPeerUser, PeerChat, PeerUser

from telegram_bot.constants import (
    BOT_TOKEN,
    DATA,
    DELETE_FAIL,
    DELETE_SUCCESS,
    EDIT_FAIL,
    FLAGGED_MESSAGE,
    FROM_GROUP,
    IS_SUCCESS,
    MESSAGE,
    RECORD_NF,
    ROOM_ID,
    SENDER_ID,
    SENDER_NAME,
    STATUS,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
    TELEGRAM_MSG_ID,
    WEBSOCKET_ROOM_NAME,
)
from telegram_bot.logger import logger
from telegram_bot.utils import exception, increment_messages_count

from .models import (
    BotIndividual,
    Chat,
    ChatBot,
    FlaggedMessage,
    Individual,
    Message,
    UserChatUnread,
)
from .serializers import (
    ChatBotSerializer,
    FlaggedMessageSerializer,
    IndividualDetailSerializer,
    MessageSerializer,
)


@asynccontextmanager
async def start_bot_client() -> TelegramClient:
    """
    Returns a TelegramClient for bot
    """
    try:
        bot = TelegramClient("bot-django", TELEGRAM_API_ID, TELEGRAM_API_HASH)
        bot = await bot.start(bot_token=BOT_TOKEN)
        yield bot
    finally:
        await bot.disconnect()


@exception
async def send_msg(data):
    """
    Sends the message to the particular chat
    """
    async with start_bot_client() as bot:
        current_bot = await bot.get_me()
        data[SENDER_ID] = current_bot.id
        data[SENDER_NAME] = current_bot.first_name

        if data[FROM_GROUP]:
            receiver = await bot.get_entity(PeerChat(int(data[ROOM_ID])))
        else:
            access_hash = Individual.objects.get(id=data[ROOM_ID]).access_hash
            receiver = InputPeerUser(int(data[ROOM_ID]), int(access_hash))
        msg_inst = await bot.send_message(receiver, data[MESSAGE])
        data[TELEGRAM_MSG_ID] = msg_inst.id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            increment_messages_count(serializer)
            # incrementing the unread count for all the admin users
            UserChatUnread.objects.filter(room_id=int(data[ROOM_ID])).update(
                unread_count=F("unread_count") + 1
            )

            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                WEBSOCKET_ROOM_NAME, {"type": "chat_message", MESSAGE: serializer.data}
            )

    return {
        DATA: {MESSAGE: serializer.data, IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


@exception
async def get_dialog(user_id):
    """
    Returns dialogs if the user is authorized
    """
    chats = ChatBot.objects.all()
    chats_serializer = ChatBotSerializer(chats, many=True)
    chat_unread = UserChatUnread.objects.filter(user_id=user_id)

    # Adding Unread count with each chat
    for chat in chats_serializer.data:
        chat["chat"]["unread_count"] = chat_unread.filter(room_id=chat["chat"]["id"])[
            0
        ].unread_count
        for indi in chat["bot"]["bot_individuals"]:
            indi["individual"]["unread_count"] = chat_unread.filter(
                room_id=indi["individual"]["id"]
            )[0].unread_count

    return {
        DATA: {"dialogs": chats_serializer.data, IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


@exception
async def get_messages(room_id, user_id, limit, offset):
    """
    Returns the messages
    """
    if limit and offset:
        data = Message.objects.filter(room_id=room_id).order_by("-date")[
            int(offset) : int(offset) + int(limit)
        ]
    elif limit:
        data = Message.objects.filter(room_id=room_id).order_by("-date")[: int(limit)]
    else:
        data = Message.objects.filter(room_id=room_id).order_by("-date")
    serializer = MessageSerializer(data, many=True)

    if data and data[0].from_group:
        individuals_id = extract_individual_ids(room_id)
        for msg in serializer.data:
            if msg[SENDER_ID] in individuals_id:
                msg["is_link"] = True

    # Resetting the unread count to 0 for the logged in admin user.
    UserChatUnread.objects.filter(user_id=user_id, room_id=room_id).update(
        unread_count=0
    )

    return {
        DATA: {"messages": serializer.data[::-1], IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


def extract_individual_ids(chat_id):
    # Extracting all the individuals id who are in conversation with the bot
    individuals_id = []
    bot = ChatBot.objects.get(chat__id=chat_id)
    individuals = BotIndividual.objects.filter(bot__id=bot.bot.id)
    for indi in individuals:
        individuals_id.append(indi.individual.id)
    return individuals_id


@exception
async def get_flagged_messages(limit, offset):
    """
    Retrieve flagged messages
    """
    if limit and offset:
        data = FlaggedMessage.objects.all().order_by("-date")[
            int(offset) : int(offset) + int(limit)
        ]
    elif limit:
        data = FlaggedMessage.objects.all().order_by("-date")[: int(limit)]
    else:
        data = FlaggedMessage.objects.all().order_by("-date")
    serializer = FlaggedMessageSerializer(data, many=True)
    return {
        DATA: {FLAGGED_MESSAGE: serializer.data[::-1], IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


@exception
async def create_flagged_message(data):
    """
    Saves the flagged message
    """
    serializer = FlaggedMessageSerializer(data=data)
    if serializer.is_valid():
        serializer.create(validated_data=data)

    message = Message.objects.get(pk=data["message"])
    message.is_flagged = True
    message.save()
    return {
        DATA: {FLAGGED_MESSAGE: data, IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


@exception
async def delete_flagged_message(id):
    """
    Deletes the flagged message
    """
    try:
        flagged_message = FlaggedMessage.objects.get(pk=id)
    except FlaggedMessage.DoesNotExist:
        return {
            DATA: {MESSAGE: RECORD_NF, IS_SUCCESS: False},
            STATUS: status.HTTP_404_NOT_FOUND,
        }

    if flagged_message.delete():
        message = Message.objects.get(pk=flagged_message.message.id)
        message.is_flagged = False
        message.save()
        return {
            DATA: {MESSAGE: DELETE_SUCCESS, IS_SUCCESS: True},
            STATUS: status.HTTP_200_OK,
        }
    return {
        DATA: {MESSAGE: DELETE_FAIL, IS_SUCCESS: False},
        STATUS: status.HTTP_400_BAD_REQUEST,
    }


def schedule_messages(xlsx_file):
    """
    Schedule the messages in bulk and
    returns erroneous sheets and rows if any
    """

    def is_blank(val):
        return val is None or val == ''

    book = tablib.Databook()
    book.load(xlsx_file, "xlsx")
    sheets = json.loads(book.export("json"))
    bad_rows = defaultdict(list)
    bad_titles = []
    for sheet in sheets:
        try:
            receiver_id = int(sheet["title"].split('|')[:-1])
            chat = Chat.objects.get(id=receiver_id)
        except (Chat.DoesNotExist, TypeError, ValueError):
            bad_titles.append(sheet["title"])
            continue

        start_date_time = parse(f"{chat.start_date} {chat.start_time}")
        for n, row in enumerate(sheet["data"], start=1):
            if is_blank(row["Days"]) or is_blank(row["Message"]):
                bad_rows[sheet["title"]].append(n)
                continue
            schedule, __ = ClockedSchedule.objects.get_or_create(
                clocked_time=start_date_time + timedelta(days=row["Days"]),
            )
            PeriodicTask.objects.create(
                clocked=schedule,
                name=str(uuid.uuid4()),
                task="mpact.tasks.send_msgs",
                args=json.dumps([receiver_id, row["Message"]]),
                one_off=True,
            )

    return {
        DATA: {
            MESSAGE: 'Messages have been scheduled',
            'bad titles': bad_titles,
            'bad rows': bad_rows,
            IS_SUCCESS: True,
        },
        STATUS: status.HTTP_200_OK,
    }


@exception
async def edit_message(room_id, data):
    """
    Returns the updated message
    """
    async with start_bot_client() as bot:
        msg_inst = Message.objects.get(id=data["message_id"])
        if msg_inst.from_group:
            receiver = await bot.get_entity(PeerChat(room_id))
        else:
            receiver = await bot.get_entity(PeerUser(room_id))

        msg = await bot.get_messages(receiver, ids=msg_inst.telegram_msg_id)
        try:
            await bot.edit_message(msg, data[MESSAGE])
        except MessageIdInvalidError:
            logger.exception(exception)
            return {
                DATA: {MESSAGE: EDIT_FAIL, IS_SUCCESS: False},
                STATUS: status.HTTP_400_BAD_REQUEST,
            }
        msg_inst.message = data[MESSAGE]
        msg_inst.save()

    return {
        DATA: {MESSAGE: data, IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


@exception
async def get_individual_details(individual_id):
    """
    Return the individual details
    """
    try:
        individual_details = Individual.objects.get(id=individual_id)
    except Individual.DoesNotExist:
        return {
            DATA: {MESSAGE: RECORD_NF, IS_SUCCESS: False},
            STATUS: status.HTTP_404_NOT_FOUND,
        }

    serializer = IndividualDetailSerializer(individual_details)
    return {
        DATA: {"individual_details": serializer.data, IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


@exception
async def update_individual_details(individual_id, data):
    """
    Return the updated individual details
    """
    try:
        individual_details = Individual.objects.get(id=individual_id)
    except Individual.DoesNotExist:
        return {
            DATA: {MESSAGE: RECORD_NF, IS_SUCCESS: False},
            STATUS: status.HTTP_404_NOT_FOUND,
        }

    serializer = IndividualDetailSerializer(individual_details, data=data)
    if serializer.is_valid():
        serializer.save()
        result = {
            DATA: {"individual_details": serializer.data, IS_SUCCESS: True},
            STATUS: status.HTTP_200_OK,
        }
    else:
        result = {
            DATA: {MESSAGE: serializer.errors, IS_SUCCESS: False},
            STATUS: status.HTTP_400_BAD_REQUEST,
        }
    return result
