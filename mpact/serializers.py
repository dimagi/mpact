from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    Bot,
    BotIndividual,
    Chat,
    ChatBot,
    FlaggedMessage,
    Individual,
    Message,
    User,
)


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = ["id", "username", "first_name", "last_name", "messages_count"]


class BotIndividualSerializer(serializers.ModelSerializer):
    individual = IndividualSerializer(required=True, many=False)

    class Meta:
        model = BotIndividual
        fields = ["individual"]


class BotSerializer(serializers.ModelSerializer):
    bot_individuals = BotIndividualSerializer(required=True, many=True)

    class Meta:
        model = Bot
        fields = ["id", "username", "bot_individuals"]


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "title", "messages_count", "participant_count"]


class ChatBotSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    bot = BotSerializer(read_only=True)

    class Meta:
        model = ChatBot
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    is_link = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = Message
        exclude = []
        read_only_fields = ["id", "date"]


class FlaggedMessageSerializer(serializers.ModelSerializer):
    message = MessageSerializer(read_only=True)

    class Meta:
        model = FlaggedMessage
        exclude = []

    def create(self, validated_data):
        message = validated_data["message"]
        msg_inst = Message.objects.get(id=message)

        FlaggedMessage.objects.create(
            message=msg_inst,
            group_id=validated_data.get("group_id", None),
        )
        return validated_data


class IndividualDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        exclude = ["access_hash", "bots"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user = User.objects.get(pk=token["user_id"])
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["username"] = user.username
        return token
