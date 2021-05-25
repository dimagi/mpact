# mPACT

A Telegram-based expert support system

# Telegram configuration

The following steps are required to create a bot for use in any project:

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

# Development Quickstart with Docker

Install docker and docker-compose.

## 1. Set Environment Variables

`cp .env.dev.example .env.dev`

Fill in the appropriate values as needed.

## 2. Perform first-time setup and start services

```bash
make init
```

Enter user details to create your first superuser, and you're done!

Open [localhost:8000](http://localhost:8000) in a browser and skip to "Creating a new chat group".

Note, that for subsequent runs, you can just run

```bash
make start
```

or

```bash
docker-compose up
```

Additionally, if you need to restart processes (edits are not automatically picked up by celery and the bot) you can run:

```bash
make start
```

More details on available commands can be found by running:

```bash
make
```

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

Chats are associated with a set of `ScheduledMessage` objects, which represent the schedule
of messages to go out. All previous scheduled messages are disabled when a new schedule is uploaded.

You can test scheduling by running the following commands. Get `<container_id>` from running `docker ps`.

```bash
docker cp /path/to/mpact_schedules.xlsx <container_id>:/mpact_schedules.xlsx
docker-compose exec web ./manage.py upload_schedule /mpact_schedules.xlsx 
```

The actual sending of messages is managed via [`django-celery-beat`](https://django-celery-beat.readthedocs.io/en/latest/).

When schedules are uploaded, once-off `PeriodicTask` objects are created for each row in the schedule.
These will call `tasks.send_msgs` with the appropriate arguments for the chat.

# Deployment

## Demo / Test environment

A demo environment has been stood up on Heroku using [Heroku's container support](https://devcenter.heroku.com/categories/deploying-with-docker).
The environment can be found at [http://mpact-demo.herokuapp.com/](http://mpact-demo.herokuapp.com/)

Configuration for the environment can be found in the `heroku.yml` file in repository root.
The application uses Docker containers built from the `Dockerfile.heroku` file in the repository root.

The `heroku.yml` file can also be used to deploy new environments. The instructions are:

1. Install the `heroku` command line tool and connect it to your account.
2. Create a new heroku application.   
3. Run `heroku stack:set container`
4. Configure your project environment variables. This can be done in the "Settings" tab in the heroku dashboard,
   or via the CLI by running `heroku config:set <var>=<value>`. Most of the variables used in development
   are also required for production, including `BOT_TOKEN`, `BOT_USERNAME`, `TELEGRAM_API_HASH`, `TELEGRAM_API_ID`,
   and `SECRET_KEY`. Additionally `DJANGO_SETTINGS_MODULE` should be set to `telegram_bot.settings_heroku`.
5. Deploy - either by using heroku's git support or connecting it directly to the git repository.
6. Create DB and superuser: `heroku run python manage.py migrate`, `heroku run python manage.py createsuperuser`

The current demo site is configured to automatically update with every commit to the `main` branch on github.
