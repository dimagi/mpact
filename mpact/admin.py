from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db import models
from django.forms import ChoiceField
from django_celery_beat.admin import PeriodicTask, PeriodicTaskAdmin, PeriodicTaskForm

from .models import (
    Bot,
    BotIndividual,
    Chat,
    ChatBot,
    Individual,
    Message,
    Profile,
    FlaggedMessage,
)

admin.site.register(Chat)
admin.site.register(Bot)
admin.site.register(Individual)
admin.site.register(ChatBot)
admin.site.register(BotIndividual)
admin.site.register(Message)
admin.site.register(FlaggedMessage)


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    inlines = (UserProfileInline,)


class CustomPeriodicTask(PeriodicTask):
    message = models.TextField(
        blank=True,
        verbose_name="Message",
        help_text="Enter the Message",
    )


class CustomPeriodicForm(PeriodicTaskForm):
    args = ChoiceField(
        label="Chat",
        required=False,
    )

    class Meta:
        model = CustomPeriodicTask
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        groups = [(c.id, c.title) for c in Chat.objects.all()]
        individuals = [(i.id, i.first_name) for i in Individual.objects.all()]
        self.fields['args'].choices = [
            ("chat", groups),
            ("individual", individuals),
        ]

    def clean_args(self):
        val = self.cleaned_data["args"]
        # Concatinating chat id and message and storing in args
        self.cleaned_data["args"] = f"""[{val}, "{self.cleaned_data['message']}"]"""
        return self._clean_json("args")


class PeriodicAdmin(PeriodicTaskAdmin):
    form = CustomPeriodicForm
    model = CustomPeriodicTask
    # added message in the Arguments
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "regtask",
                    "task",
                    "enabled",
                    "description",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "interval",
                    "crontab",
                    "solar",
                    "clocked",
                    "start_time",
                    "last_run_at",
                    "one_off",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Arguments",
            {
                "fields": ("message", "args", "kwargs"),
                "classes": ("extrapretty", "wide", "collapse", "in"),
            },
        ),
        (
            "Execution Options",
            {
                "fields": (
                    "expires",
                    "expire_seconds",
                    "queue",
                    "exchange",
                    "routing_key",
                    "priority",
                    "headers",
                ),
                "classes": ("extrapretty", "wide", "collapse", "in"),
            },
        ),
    )


admin.site.register(CustomPeriodicTask, PeriodicAdmin)
