from channels.http import AsgiHandler
from channels.routing import ChannelNameRouter, ProtocolTypeRouter
from mpact.consumers import ConnectionConsumer
from mpact.routing import websockets

application = ProtocolTypeRouter(
    {
        "http": AsgiHandler(),
        "websocket": websockets,
        "channel": ChannelNameRouter(
            {
                "chat": ConnectionConsumer,
            }
        ),
    }
)
