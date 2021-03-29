import json

from channels.generic.websocket import AsyncWebsocketConsumer
from telegram_bot.constants import MESSAGE, WEBSOCKET_ROOM_NAME


class ConnectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = WEBSOCKET_ROOM_NAME
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def chat_message(self, event):
        message = event[MESSAGE]
        # Send message to connected clients
        await self.send(text_data=json.dumps({MESSAGE: message}))

    async def disconnect(self, code):
        # Leave room group
        self.channel_layer.group_discard(self.room_name, self.channel_name)
