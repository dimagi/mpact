import os

from django.core.management import BaseCommand
from django.urls import reverse

from mpact.constants import MESSAGE
from mpact.services import updater


class Command(BaseCommand):
    help = ('Set the URL to receive incoming updates from Telegram.')

    def handle(self, *args, **options):
        success = set_webhook()
        print('OK' if success else 'Unable to set webhook')


def set_webhook() -> bool:
    local_url = 'http://localhost:8000' + reverse("listen_msg")
    webhook_url = os.environ.get('WEBHOOK_URL') or local_url
    success = updater.bot.setWebhook(webhook_url, allowed_updates=[MESSAGE])
    return success
