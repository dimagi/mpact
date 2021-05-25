mPACT Administration
====================

## Creating a new chat group

1. In Telegram, open the menu and choose "New Group".
1. Add the bot to the group. It will not appear as a contact. You will
   need to type its username (the same username as the BOT_USERNAME
   environment variable).
1. Give your new group a name.

The bot will be notified of its new group, and the group will be added
to the database. The next time you log into mPACT, the group will appear
in the left panel.


## Scheduling

Chats are associated with a set of `ScheduledMessage` objects, which
represent the schedule of messages to go out. All previous scheduled
messages are disabled when a new schedule is uploaded.

You can test scheduling in a development environment by running the
following commands. Get `<container_id>` from running `docker ps`.

```bash
docker cp /path/to/mpact_schedules.xlsx <container_id>:/mpact_schedules.xlsx
docker-compose exec web ./manage.py upload_schedule /mpact_schedules.xlsx 
```

The actual sending of messages is managed via
[`django-celery-beat`](https://django-celery-beat.readthedocs.io/en/latest/).

When schedules are uploaded, once-off `PeriodicTask` objects are created
for each row in the schedule. These will call `tasks.send_msgs` with the
appropriate arguments for the chat.
