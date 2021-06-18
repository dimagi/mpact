from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


def validate_phone(username):
    if username[0] != "+":
        raise ValidationError("Phone number should start with '+'.")
    return username


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number is invalid.",
    )
    phone = models.CharField(max_length=20, validators=[phone_regex, validate_phone])


class ChatBase(BaseModel):
    """
    Represents a telegram chat, which could be a group or 1:1 chat (individual)
    """
    id = models.IntegerField(primary_key=True, help_text='The Telegram ID of the chat')
    messages_count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class GroupChat(ChatBase):
    """
    Represents a telegram group
    """
    title = models.TextField()
    participant_count = models.IntegerField(default=0)
    schedule_start_date = models.DateField(default=timezone.now)
    schedule_start_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} - {self.title}"

    def save(self, *args, **kwargs):
        try:
            # self.pk is a Telegram ID
            previous_model = GroupChat.objects.get(pk=self.pk)
            schedule_changed = (
                self.schedule_start_date != previous_model.schedule_start_date or
                self.schedule_start_time != previous_model.schedule_start_time
            )
        except GroupChat.DoesNotExist:
            # `previous_model` doesn't exist because this GroupChat is new
            schedule_changed = False

        super().save(*args, **kwargs)
        if schedule_changed:
            from mpact.scheduling import rebuild_schedule_for_group
            rebuild_schedule_for_group(self)


class Bot(BaseModel):
    id = models.IntegerField(primary_key=True)
    username = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField(null=True)
    chats = models.ManyToManyField(GroupChat, through="ChatBot")

    def __str__(self):
        return f"{self.id} - {self.username}"


class ChatBot(BaseModel):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

    def __str__(self):
        return f"chat_id: {self.chat.id} - bot_username: {self.bot.username}"


class IndividualChat(ChatBase):
    """
    Represents a telegram user (and their 1:1 conversations with bots).
    """
    username = models.TextField(null=True)
    first_name = models.TextField()
    last_name = models.TextField(null=True)
    access_hash = models.TextField()
    study_id = models.TextField(null=True)
    age = models.IntegerField(null=True)
    gender = models.TextField(null=True)
    address = models.TextField(null=True)
    notes = models.TextField(null=True)
    bots = models.ManyToManyField(Bot, through="BotIndividual")

    def __str__(self):
        return f"{self.id} - {self.first_name}"


class BotIndividual(BaseModel):
    bot = models.ForeignKey(
        Bot, related_name="bot_individuals", on_delete=models.CASCADE
    )
    individual = models.ForeignKey(IndividualChat, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"individual_id: {self.individual.id} - bot_username: {self.bot.username}"
        )


class Message(BaseModel):
    telegram_msg_id = models.IntegerField()
    sender_id = models.IntegerField()
    sender_name = models.TextField()
    room_id = models.IntegerField()
    message = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)
    from_group = models.BooleanField()
    is_flagged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_id} - {self.sender_name} - {self.message}"


class FlaggedMessage(BaseModel):
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    group_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.message.id} - {self.message.room_id}"


class UserChatUnread(BaseModel):
    user_id = models.IntegerField()
    room_id = models.IntegerField()
    unread_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user_id", "room_id")

    def __str__(self):
        return f"{self.user_id} - {self.room_id} - {self.unread_count}"


class ScheduledMessage(BaseModel):
    """
    Tracks the "schedule" for a particular group chat.
    """
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='scheduled_messages')
    day = models.PositiveIntegerField(help_text='How many days after a group start date to send this message')
    message = models.TextField()
    comment = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        group_changed = False
        schedule_changed = False
        previous_model = None
        if self.pk:
            previous_model = ScheduledMessage.objects.get(pk=self.pk)
            group_changed = self.group != previous_model.group
            at_least_one_enabled = self.enabled or previous_model.enabled
            schedule_changed = (
                at_least_one_enabled and (
                    group_changed or
                    self.enabled != previous_model.enabled or
                    self.day != previous_model.day or
                    self.message != previous_model.message
                )
            )

        super().save(*args, **kwargs)
        if schedule_changed:
            from mpact.scheduling import rebuild_schedule_for_group
            rebuild_schedule_for_group(self.group)
            if group_changed:
                rebuild_schedule_for_group(previous_model.group)
