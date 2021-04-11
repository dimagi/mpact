from django.core.management.base import BaseCommand

from mpact.services import schedule_messages


class Command(BaseCommand):
    help = 'Upload a schedule from an excel file'

    def add_arguments(self, parser):
        parser.add_argument('schedule_file')

    def handle(self, schedule_file, *args, **options):
        with open(schedule_file, 'rb') as f:
            print(schedule_messages(f))
