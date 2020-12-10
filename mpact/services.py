from contextlib import asynccontextmanager

from django.contrib.auth.models import User
from django.http import HttpResponse
from telethon import TelegramClient
from telethon.errors import (
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)

from .constants import (
    BOT_TOKEN,
    CHAT_ID,
    CODE,
    INVALID_CODE,
    LOGOUT,
    MESSAGE,
    MESSAGE_SENT,
    NOT_AUTHORIZED,
    PASSWORD,
    PASSWORD_REQUIRED,
    PHONE,
    PHONE_CODE_HASH,
    PHONE_NOT_REGISTERED,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
)
from .logger import logger


@asynccontextmanager
async def get_anon_client():
    """
    TelegramClient is already an async context manager. This context
    manager connect to the telegram and logs exceptions.
    """
    try:
        client = get_telegram_client("anon")
        await client.connect()
        yield client
    except Exception as exception:
        logger.exception(exception)
        raise
    finally:
        await client.disconnect()


def start_bot_client() -> TelegramClient:
    """
    Returns a TelegramClient for bot
    """
    return get_telegram_client("bot").start(bot_token=BOT_TOKEN)


def get_telegram_client(session_name: str) -> TelegramClient:
    return TelegramClient(session_name, TELEGRAM_API_ID, TELEGRAM_API_HASH)


async def login(data):
    """
    Returns the logged in user details or hash code & other details for code request
    """
    user = get_or_none(User, profile__phone=data[PHONE])
    if not user:
        return PHONE_NOT_REGISTERED

    async with get_anon_client() as client:
        if PASSWORD in data:
            user_details = await client.sign_in(
                password=data[PASSWORD],
            )
            await client.disconnect()
            return user_details
        elif CODE in data:
            try:
                user_details = await client.sign_in(
                    phone=data[PHONE],
                    code=data[CODE],
                    phone_code_hash=data[PHONE_CODE_HASH],
                )
            except (PhoneCodeInvalidError, PhoneCodeExpiredError):
                return INVALID_CODE
            except SessionPasswordNeededError:
                return PASSWORD_REQUIRED
            await client.disconnect()
            return user_details
        # sending otp to phone number
        code_request = await client.send_code_request(data[PHONE])
        return code_request


async def logout():
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            await client.log_out()
    return LOGOUT


async def send_msg(data):
    """
    Sends the message to the particular chat
    """
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            async with await start_bot_client() as bot:
                await bot.send_message(data[CHAT_ID], data[MESSAGE])
            return MESSAGE_SENT
        return NOT_AUTHORIZED


async def get_dialog():
    """
    Returns dialogs if the user is authorized
    """
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            dialogs = await client.get_dialogs()
            return dialogs
        return NOT_AUTHORIZED


def get_or_none(model, **kwargs):
    """
    Returns model object if exists else None
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
