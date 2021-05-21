from .settings import *
import django_heroku

django_heroku.settings(locals())

# redis setup
REDIS_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static_out')

# fix ssl mixed content issues
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = False
ALLOWED_HOSTS = [
    'mpact.herokuapp.com',
]
