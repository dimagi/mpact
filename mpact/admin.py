from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from django.forms import ChoiceField
from django_celery_beat.admin import PeriodicTask, PeriodicTaskAdmin, PeriodicTaskForm

from .models import (
    Bot,
    BotIndividual,
    GroupChat,
    ChatBot,
    FlaggedMessage,
    IndividualChat,
    Message,
    UserChatUnread,
    ScheduledMessage,
)

# clean up unused models from admin
admin.site.unregister(Group)

admin.site.register(GroupChat)
admin.site.register(Bot)
admin.site.register(IndividualChat)
admin.site.register(ChatBot)
admin.site.register(BotIndividual)
admin.site.register(FlaggedMessage)
admin.site.register(UserChatUnread)


@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    list_display = ['message', 'day', 'group', 'comment', 'enabled']
    list_filter = ['group', 'enabled']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message', 'date', 'telegram_msg_id', 'sender_id', 'sender_name', 'room_id']
    list_filter = ['date', 'sender_id', 'room_id']
