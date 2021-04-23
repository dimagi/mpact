# mPACT

A Telegram-based expert support system

## Telegram configuration

1. Download Telegram to your phone and set it up.

1. Follow instructions for [obtaining your Telegram API 
   key](https://core.telegram.org/api/obtaining_api_id). Note your API ID 
   and the API hash.

1. [Create a bot](https://core.telegram.org/bots#6-botfather) by messaging 
   the botfather. Note your bot's username and token.

1. **Optional**: [Disable privacy 
   mode](https://www.teleme.io/articles/group_privacy_mode_of_telegram_bots) 
   for your bot to ensure that it can see all messages. If you do not wish to 
   disable [privacy mode](https://core.telegram.org/bots#privacy-mode), ensure 
   that the bot is added as an admin to each group. If it was added as a non-admin, 
   you will need to re-add the bot.

# Quickstart with Docker

Install docker and docker-compose.

## 1. Set Environment Variables

`cp .env.dev.example .env.dev`

Fill in the appropriate values as needed.

## 2. Start services

```bash
docker-compose up
```

## 3. Perform first-time setup

```bash
make init
```

Enter user details to create your first superuser, and you're done!

Open [localhost:8000](http://localhost:8000) in a browser and skip to "Creating a new chat group".


# Legacy set up instructions

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
       export ALLOWED_HOSTS='127.0.0.1,localhost'
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

    (redis) $ redis-server
    (bot) $ python3 mpact_bot.py
    (worker) $ celery -A telegram_bot worker -l info --pool=solo
    (beat) $ celery -A telegram_bot beat -l info \
             --scheduler django_celery_beat.schedulers:DatabaseScheduler
    (server) $ python3 manage.py runserver
    (client) $ npm run dev


# Creating a new chat group

1. Ensure **mpact_bot.py** is running.
2. In Telegram, open the menu and choose "New Group".
3. Add the bot to the group. It will not appear as a contact. You will
   need to type its username (the same username as the BOT_USERNAME
   environment variable).
4. Give your new group a name.

The bot will be notified of its new group, and the group will be added
to the database. The next time you log into mPACT, the group will appear
in the left panel.


# Technical Documentation

*This section is a work in progress.*

## Scheduling

You can test scheduling by running the following commands. Get `<container_id>` from running `docker ps`.

```bash
docker cp /path/to/mpact_schedules.xlsx <container_id>:/mpact_schedules.xlsx
docker-compose exec web ./manage.py upload_schedule /mpact_schedules.xlsx 
```

Scheduling is managed via [`django-celery-beat`](https://django-celery-beat.readthedocs.io/en/latest/).

When schedules are uploaded, once-off `PeriodicTask` objects are created for each row in the schedule.
These will call `tasks.send_msgs` with the appropriate arguments for the chat.

As of now there is no way to link back to the schedule once they are created. Meaning that
it's impossible to "deschedule" or "replace" something after it's been uploaded.
Additionally, this means that the download schedule button will always return a blank sheet,
even if a schedule exists for the chat.


[direnv]: https://github.com/direnv/direnv/#direnv----unclutter-your-profile
[tmux]: https://github.com/tmux/tmux#welcome-to-tmux
