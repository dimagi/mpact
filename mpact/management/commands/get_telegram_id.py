from django.core.management.base import BaseCommand

from mpact import services
from mpact.views import new_or_current_event_loop


class Command(BaseCommand):
    help = 'Gets a telegram ID from a phone number'

    def add_arguments(self, parser):
        parser.add_argument('phone_number')

    def handle(self, phone_number, *args, **options):
        telegram_id = new_or_current_event_loop().run_until_complete(services.get_telegram_id(phone_number))
        print(f'ID is {telegram_id}')
