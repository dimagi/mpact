from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


def validate_phone(username):
    if username[0] != "+":
        raise ValidationError("Phone number should start with '+'.")
    return username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number is invalid.",
    )
    phone = models.CharField(max_length=20, validators=[phone_regex, validate_phone])


class Chat(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.id} - {self.title}"


class Bot(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField(null=True)
    chats = models.ManyToManyField(Chat, through="ChatBot")

    def __str__(self):
        return f"{self.id} - {self.username}"


class ChatBot(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

    def __str__(self):
        return f"chat_id: {self.chat.id} - bot_username: {self.bot.username}"


class Individual(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.TextField(null=True)
    first_name = models.TextField()
    last_name = models.TextField(null=True)
    access_hash = models.TextField()
    study_id = models.TextField(null=True)
    age = models.TextField(null=True)
    gender = models.TextField(null=True)
    address = models.TextField(null=True)
    notes = models.TextField(null=True)
    bots = models.ManyToManyField(Bot, through="BotIndividual")

    def __str__(self):
        return f"{self.id} - {self.first_name}"


class BotIndividual(models.Model):
    bot = models.ForeignKey(
        Bot, related_name="bot_individuals", on_delete=models.CASCADE
    )
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"individual_id: {self.individual.id} - bot_username: {self.bot.username}"
        )


class Message(models.Model):
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    sender = models.IntegerField()
    message = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)
    is_flagged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.individual.first_name} - {self.sender}"


class FlaggedMessage(models.Model):
    room_id = models.IntegerField()
    message_id = models.IntegerField()
    first_name = models.TextField()
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    is_group = models.BooleanField()
    # If the message is being flagged from individual chat,
    # group_id is needed to link the flagged message screen to individual chat
    group_id = models.IntegerField(null=True)

    class Meta:
        unique_together = ("room_id", "message_id")

    def __str__(self):
        return f"{self.room_id} - {self.first_name} - {self.message}"
