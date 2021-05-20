import os
import django_heroku
from django.core.management.utils import get_random_secret_key

django_heroku.settings(locals())

SECRET_KEY = os.getenv('SECRET_KEY', default=get_random_secret_key())

# fix ssl mixed content issues
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = False
ALLOWED_HOSTS = [
    'mpact.herokuapp.com',
]
