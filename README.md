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

# mPACT Administration

See [the Admin documentation](docs/index.md) for more information on how
to administrate your deployed mPACT instance.
