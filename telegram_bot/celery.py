import os

from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot.settings")
celery_app = Celery("telegram_bot")
# Celery will apply all configuration keys with defined namespace
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
# Load tasks from all registered apps
celery_app.autodiscover_tasks()
