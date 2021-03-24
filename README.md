# mPACT

A Telegram-based expert support system


## Installing a development environment

1. Install prerequisite packages

       $ sudo apt install python3.8-venv

2. Create and activate a Python virtual environment

       $ python3.8 -m venv venv
       $ source venv/bin/activate

3. Install requirements

       $ pip install -r requirements.txt
       $ npm install


## Set Environment Variables

Secrets are set using environment variables.

You can generate a secret key with

    $ python3 -c 'import string
    import secrets
    chars = string.ascii_letters + string.digits
    key = "".join(secrets.choice(chars) for x in range(64))
    print(key)'

1. Save the environment variables in a `.envrc` file:

       $ cat > .envrc <<EOF
       export DEPLOY_ENV=dev
       export SECRET_KEY=<Django Secret Key>
       export BOT_USERNAME=<Telegram Bot Username>
       export BOT_TOKEN=<Telegram Bot Token>
       export TELEGRAM_API_ID=<Telegram API ID>
       export TELEGRAM_API_HASH=<Telegram API Hash>
       export ALLOWED_HOSTS='127.0.0.1 localhost'
       export DATABASE_URL=sqlite:///mpact.sqlite
       export SECURED_URL_SECRET_KEY=<Another Secret Key>
       export SECURITY_PASSWORD_SALT=<Password Salt>
       EOF

2. Set them. You can get this to happen [automatically][direnv], but
   doing it manually is easy:

       $ source .envrc


## First time use

The first time you run your environment, you will need to migrate the
database and create a superuser:

    $ python3 manage.py migrate
    $ python3 manage.py createsuperuser


## Run

You can run your development environment with the following commands,
each in their own terminal and/or by using a tool like [tmux][tmux].

    (redis) $ docker-compose up
    (bot) $ python3 mpact_bot.py
    (worker) $ celery -A telegram_bot worker -l info --pool=solo
    (beat) $ celery -A telegram_bot beat -l info \
             --scheduler django_celery_beat.schedulers:DatabaseScheduler
    (server) $ python3 manage.py runserver
    (client) $ npm run dev


## Creating a new chat group

1. Ensure **mpact_bot.py** is running.
2. In Telegram, open the menu and choose "New Group".
3. Add the bot to the group. It will not appear as a contact. You will
   need to type its username (the same username as the BOT_USERNAME
   environment variable).
4. Give your new group a name.

The bot will be notified of its new group, and the group will be added
to the database. The next time you log into mPACT, the group will appear
in the left panel.


[direnv]: https://github.com/direnv/direnv/#direnv----unclutter-your-profile
[tmux]: https://github.com/tmux/tmux#welcome-to-tmux
