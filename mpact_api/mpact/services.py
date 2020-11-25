from contextlib import asynccontextmanager

from telethon import TelegramClient
from telethon.hints import EntityLike

from .constants import (
    BOT_TOKEN,
    CODE,
    LOGOUT,
    MESSAGE,
    MESSAGE_SENT,
    NOT_AUTHORIZED,
    PHONE,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
)
from .logger import logger


async def login(data: dict):
    async with get_anon_client() as client:
        if CODE in data:
            user_details = await client.sign_in(code=data[CODE])
            return user_details
        else:
            # sending otp to phone number
            code_request = await client.send_code_request(data[PHONE])
            return code_request


async def logout():
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            await client.log_out()
        return LOGOUT


async def send_msg(entity: EntityLike, data: dict):
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            await client.send_message(entity, data[MESSAGE])
    return MESSAGE_SENT


async def get_dialogs():
    async with get_anon_client() as client:
        if await client.is_user_authorized():
            dialogs = await client.get_dialogs()
            return dialogs
    return NOT_AUTHORIZED


@asynccontextmanager
async def get_anon_client_with_logger():
    """
    TelegramClient is already an async context manager. This context
    manager just logs exceptions.
    """
    async with get_anon_client() as client:
        try:
            yield client
        except Exception as exception:
            logger.exception(exception)
            raise


def get_anon_client() -> TelegramClient:
    """
    Returns a TelegramClient with the session name "anon"

    .. IMPORTANT::
       Exposing a logged-in session over a web API allows **anyone** to
       use that session, not just the person who logged in!

    """
    return get_telegram_client("anon")



def start_bot_client() -> TelegramClient:
    return get_telegram_client("bot").start(bot_token=BOT_TOKEN)


def get_telegram_client(session_name: str) -> TelegramClient:
    return TelegramClient(session_name, TELEGRAM_API_ID, TELEGRAM_API_HASH)
