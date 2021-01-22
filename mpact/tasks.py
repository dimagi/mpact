from celery import shared_task
from constants import DATA, INDIVIDUAL, IS_SUCCESS, MESSAGE, MESSAGE_SENT
from telethon.tl.types import InputPeerChat, InputPeerUser

from .models import Individual
from .serializers import MessageSerializer
from .services import start_bot_client
from .views import new_or_current_event_loop


@shared_task
def send_msgs(receiver_id, message):
    return new_or_current_event_loop().run_until_complete(
        send_msg(receiver_id, message)
    )


async def send_msg(receiver_id, message):
    """
    Sends the message to the particular chat
    """
    async with await start_bot_client() as bot:
        data = {}
        current_bot = await bot.get_me()
        data["sender"] = current_bot.id
        data[INDIVIDUAL] = receiver_id
        data[MESSAGE] = message

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            access_hash = Individual.objects.get(id=receiver_id).access_hash
            receiver = InputPeerUser(int(data[INDIVIDUAL]), int(access_hash))
        else:
            receiver = InputPeerChat(int(data[INDIVIDUAL]))
        await bot.send_message(receiver, data[MESSAGE])

    return {
        DATA: {MESSAGE: MESSAGE_SENT},
        IS_SUCCESS: True,
    }
