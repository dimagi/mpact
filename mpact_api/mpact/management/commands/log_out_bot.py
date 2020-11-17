"""
Log bot out of cloud Telegram Bot API server.

Required for using a local `Telegram Bot API server`_.

The logOut command is not available as a method of the telegram.Bot
class, so this command is used to call the Telegram Bot API.


.. _Telegram Bot API server: https://github.com/tdlib/telegram-bot-api

"""
import os
from typing import Tuple
import requests
from django.core.management import BaseCommand

API_BASE_URL = 'https://api.telegram.org'


class Command(BaseCommand):
    help = ('Log bot out of cloud Telegram Bot API server.')

    def handle(self, *args, **options):
        token = os.environ['TOKEN']
        success, message = log_out(token)
        print('OK' if success else f'Logout failed: {message}')


def log_out(token: str) -> Tuple[bool, str]:
    url = f'{API_BASE_URL}/bot{token}/logOut'
    response = requests.get(url)
    return (200 >= response.status_code < 300, response.text)
