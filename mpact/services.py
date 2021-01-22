from contextlib import asynccontextmanager

from constants import (
    BOT_TOKEN,
    CODE,
    DATA,
    FIRST_NAME,
    INDIVIDUAL,
    INVALID_CODE,
    IS_SUCCESS,
    LAST_NAME,
    LOGOUT,
    MESSAGE,
    MESSAGE_SENT,
    NOT_AUTHORIZED,
    PASSWORD,
    PASSWORD_REQUIRED,
    PHONE,
    PHONE_CODE_HASH,
    PHONE_NOT_REGISTERED,
    STATUS,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
    TOKEN,
    TWO_FA_ENABLED,
    USERNAME,
)
from django.contrib.auth.models import User
from logger import logger
from rest_framework import status
from telegram_bot.settings import container
from telethon import TelegramClient
from telethon.errors import (
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)
from telethon.tl.types import InputPeerUser
from utils import encode_token, get_or_none

from .models import ChatBot, Individual, Message
from .serializers import ChatBotSerializer, MessageSerializer


@asynccontextmanager
async def client_context(phone):
    """
    TelegramClient is already an async context manager. This context
    manager connect to the telegram and logs exceptions.
    """
    try:
        client = get_telegram_client(phone)
        await client.connect()
        yield client
    except Exception as exception:
        logger.exception(exception)
        raise
    await client.disconnect()


def start_bot_client() -> TelegramClient:
    """
    Returns a TelegramClient for bot
    """
    return get_telegram_client("bot").start(bot_token=BOT_TOKEN)


def get_telegram_client(session_name: str) -> TelegramClient:
    session = container.new_session(session_name)
    return TelegramClient(session, TELEGRAM_API_ID, TELEGRAM_API_HASH)


async def login(data):
    """
    Returns the logged in user details or hash code & other details for code request
    """
    user = get_or_none(User, profile__phone=data[PHONE])
    if not user:
        NOT_AUTHORIZED[DATA][MESSAGE] = PHONE_NOT_REGISTERED
        return NOT_AUTHORIZED

    async with client_context(data[PHONE]) as client:
        if PASSWORD in data:
            return await two_factor_auth(client, data)
        elif CODE in data:
            return await validate_code(client, data)
        # sending otp to phone number
        code_request = await client.send_code_request(data[PHONE])
        return {
            DATA: {PHONE_CODE_HASH: code_request.phone_code_hash, IS_SUCCESS: True},
            STATUS: status.HTTP_200_OK,
        }


async def two_factor_auth(client, data):
    """
    Verify the password entered by the user and
    returns the user details upon successful login
    """
    user_details = await client.sign_in(
        password=data[PASSWORD],
    )
    await client.disconnect()
    return ok_response(user_details, data)


def ok_response(user_details, data):
    return {
        DATA: {
            FIRST_NAME: user_details.first_name,
            TOKEN: encode_token(
                {
                    LAST_NAME: user_details.last_name,
                    USERNAME: user_details.username,
                    PHONE: data[PHONE],
                }
            ),
            IS_SUCCESS: True,
        },
        STATUS: status.HTTP_200_OK,
    }


async def validate_code(client, data):
    """
    validate the code (OTP) & return user details and if two factor authenticated
    is enabled, it will ask for password.
    """
    try:
        user_details = await client.sign_in(
            phone=data[PHONE],
            code=data[CODE],
            phone_code_hash=data[PHONE_CODE_HASH],
        )
    except SessionPasswordNeededError:
        return {
            DATA: {MESSAGE: PASSWORD_REQUIRED, TWO_FA_ENABLED: True, IS_SUCCESS: True},
            STATUS: status.HTTP_200_OK,
        }
    except (PhoneCodeInvalidError, PhoneCodeExpiredError):
        return {
            DATA: {MESSAGE: INVALID_CODE, IS_SUCCESS: False},
            STATUS: status.HTTP_400_BAD_REQUEST,
        }
    await client.disconnect()
    return ok_response(user_details, data)


async def logout(phone):
    async with client_context(phone) as client:
        if await client.is_user_authorized():
            await client.log_out()
    return {
        DATA: {MESSAGE: LOGOUT, IS_SUCCESS: True},
        STATUS: status.HTTP_200_OK,
    }


async def send_msg(phone, data):
    """
    Sends the message to the particular chat
    """
    async with client_context(phone) as client:
        if await client.is_user_authorized():
            async with await start_bot_client() as bot:
                current_bot = await bot.get_me()
                data["sender"] = current_bot.id
                serializer = MessageSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    access_hash = Individual.objects.get(
                        id=data[INDIVIDUAL]
                    ).access_hash
                    receiver = InputPeerUser(int(data[INDIVIDUAL]), int(access_hash))
                else:
                    receiver = await client.get_entity(int(data[INDIVIDUAL]))
                await bot.send_message(receiver, data[MESSAGE])

            return {
                DATA: {MESSAGE: MESSAGE_SENT},
                STATUS: status.HTTP_200_OK,
                IS_SUCCESS: True,
            }
        return NOT_AUTHORIZED


async def get_dialog(phone):
    """
    Returns dialogs if the user is authorized
    """
    async with client_context(phone) as client:
        if await client.is_user_authorized():
            chats = ChatBot.objects.all()
            chats_serializer = ChatBotSerializer(chats, many=True)
            return {
                DATA: {"dialogs": chats_serializer.data, IS_SUCCESS: True},
                STATUS: status.HTTP_200_OK,
            }
        return NOT_AUTHORIZED


async def get_individual_msg(phone, individual_id):
    """
    Returns private chat messages if the user is authorized
    """
    async with client_context(phone) as client:
        if await client.is_user_authorized():
            data = Message.objects.filter(individual=individual_id)
            serializer = MessageSerializer(data, many=True)
            return {
                DATA: {"messages": serializer.data, IS_SUCCESS: True},
                STATUS: status.HTTP_200_OK,
            }
        return NOT_AUTHORIZED


async def get_chat_msg(phone, chat_id, limit, offset):
    """
    Returns group chat messages if the user is authorized
    """
    async with client_context(phone) as client:
        if await client.is_user_authorized():
            await client.get_dialogs()
            msgs = []
            if limit and offset:
                async for message in client.iter_messages(
                    chat_id, limit=int(limit), offset_id=int(offset)
                ):
                    extract_messages(message, msgs)
            elif limit:
                async for message in client.iter_messages(chat_id, limit=int(limit)):
                    extract_messages(message, msgs)
            else:
                async for message in client.iter_messages(chat_id):
                    extract_messages(message, msgs)

            return {
                DATA: {"messages": msgs[::-1], IS_SUCCESS: True},
                STATUS: status.HTTP_200_OK,
            }
        return NOT_AUTHORIZED


def extract_messages(message, msgs):
    if message.message:
        msgs.append(
            {
                "id": message.id,
                "sender": message.sender.first_name,
                MESSAGE: message.text,
                "date": message.date,
            }
        )
