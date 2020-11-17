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
    $ export TOKEN=<Telegram Bot Token>
    $ export BOT_USERNAME=<Telegram Bot Username>
    $ export ALLOWED_HOSTS='127.0.0.1 localhost'

## Run

    $ cd mpact_api
    $ ./manage.py runserver

## There is a script for that

It is usually easy to set environment variables once for a production
environment, and not have to do it again.

To make it just as easy for your development environment, copy the
**manage-dev.example** script to **manage-dev**, and set the
environment variables in it:

    $ cp manage-dev.example manage-dev

Open **manage-dev** in your favorite editor, and set the values of
`SECRET_KEY`, `TOKEN` and `BOT_USERNAME`.

You can generate a secret key with

    $ python3 -c 'import string
    import secrets
    chars = string.ascii_letters + string.digits
    key = "".join(secrets.choice(chars) for x in range(64))
    print(key)'

Now you can run a development server with

    $ ./manage-dev runserver

## Running a local Telegram Bot API server

Using a local Telegram Bot API server allows you to develop and test a
webhook on localhost, using any port, and without SSL.

Refer to the [telegram-bot-api](https://github.com/tdlib/telegram-bot-api)
repository on GitHub for more details and installation instructions.

To make it easy to run, copy **api-server.example** to **api-server**
and set the environment variables.

    $ cp api-server.example api-server

Open **api-server** in an editor.

Set `BASE_DIR` to the **telegram-bot-api** installation directory.

Set `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` to the values for your
app. You can find the values at <https://my.telegram.org/apps>.

Start the API server on <http://localhost:8081> with

    $ ./api-server

Or display usage and options with

    $ ./api-server --help
