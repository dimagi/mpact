from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import MESSAGE, NEW_CHAT_PARTICIPANT, NEW_CHAT_TITLE, OK, TEXT
from .logger import logger
from .services import anonymize
from .management.commands.set_webhook import set_webhook
from .telegramevents import TelegramEvents


class Webhook(APIView):
    """
    This is only called once for the webhook setup.
    """

    def get(self, request):
        success = set_webhook()
        if success:
            return Response("webhook setup ok")
        else:
            return Response("webhook setup failed")


class ListenMessages(APIView):
    """
    Telegram webhook makes a post request.
    """

    def post(self, request):
        """
        Sample ``request.data``::
        {
            "update_id": 30927953,
            "message": {
                "message_id": 51,
                "from": {
                    "id": 1229986355,
                    "is_bot": False,
                    "first_name": "John",
                    "last_name": "Walter",
                    "language_code": "en"
                },
                "chat": {
                    "id": -433354696,
                    "title": "Testing Group",
                    "type": "group",
                    "all_members_are_administrators": True
                },
                "date": 1604317469,

                /** Someone sends a message in a group: */
                "text": "Hello, How are you?"

                /** Someone joins a chat: */
                "new_chat_participant": {
                    "id": 1321604047,
                    "is_bot": True,
                    "first_name": "demo_bot",
                    "username": "test_bot"
                },
                "new_chat_member": {
                    "id": 1321604047,
                    "is_bot": True,
                    "first_name": "demo_bot",
                    "username": "test_bot"
                },
                "new_chat_members": [
                    {
                            "id": 1321604047,
                            "is_bot": True,
                            "first_name": "demo_bot",
                            "username": "test_bot"
                    }
                ]

                /** Someone leaves a chat: */
                "left_chat_member": {
                    "id": 879250491,
                    "is_bot": False,
                    "first_name": "John",
                    "last_name": "Walter"
                }
            }
        }
        """
        try:
            message = request.data[MESSAGE]
            event = TelegramEvents(message)

            if NEW_CHAT_PARTICIPANT in message:
                event.new_chat_participant()
            elif NEW_CHAT_TITLE in message:
                event.new_chat_title()
            elif TEXT in message:
                event.text()
            else:
                raise ValueError(
                    f"Unrecognized event in message: {anonymize(message)!r}"
                )

        except Exception as exeception:
            logger.exception(exeception)

        return Response(OK)
