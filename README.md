# mpact

A Telegram-based expert support system

## Installing a development environment

1. Install prerequisite packages

       $ sudo apt install python3.8-venv

2. Create and activate a Python virtual environment

       $ python3.8 -m venv venv
       $ source venv/bin/activate

3. Install requirements

       $ pip install -r requirements.txt

## Set Environment Variables

    $ export SECRET_KEY=<Django Secret Key>
    $ export BOT_TOKEN=<Telegram Bot Token>
    $ export TELEGRAM_API_ID=<Telegram API ID>
    $ export TELEGRAM_API_HASH=<Telegram API Hash>
    $ export ALLOWED_HOSTS='127.0.0.1 localhost'
    $ export SECURED_URL_SECRET_KEY="1234"
    $ export SECURITY_PASSWORD_SALT="1234"


## There is a script for that

It is usually easy to set environment variables once for a production
environment, and not have to do it again.

To make it just as easy for your development environment, copy the
**manage-dev.example** script to **manage-dev**, and set the
environment variables in it:

    $ cp manage-dev.example manage-dev

Open **manage-dev** in your favorite editor, and set the values of
`SECRET_KEY`, `BOT_TOKEN`, `TELEGRAM_API_ID`,  `TELEGRAM_API_HASH`, `SECURED_URL_SECRET_KEY` and `SECURITY_PASSWORD_SALT`

You can generate a secret key with

    $ python3 -c 'import string
    import secrets
    chars = string.ascii_letters + string.digits
    key = "".join(secrets.choice(chars) for x in range(64))
    print(key)'


## Run

Now you can run a development server with

    $ npm install
    $ npm run dev
    $ docker-compose up
    $ celery -A telegram_bot beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
    $ ./manage-dev runserver

Create a super user with the below command

    $ ./manage-dev createsuperuser
