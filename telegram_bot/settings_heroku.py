import django_heroku
django_heroku.settings(locals())

# fix ssl mixed content issues
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = False
ALLOWED_HOSTS = [
    'mpact.herokuapp.com',
]
