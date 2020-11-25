import asyncio

from django.http import HttpResponse
from rest_framework.views import APIView

from .services import get_dialogs, login, logout, send_msg


class Login(APIView):
    """
    It is used to login into telegram
    """

    def post(self, request):
        # request.data will contain phone or code.
        loop = get_event_loop()
        return HttpResponse(loop.run_until_complete(login(request.data)))


class Logout(APIView):
    """
    It is used to log out from telegram.
    """

    def get(self, request):
        loop = get_event_loop()
        return HttpResponse(loop.run_until_complete(logout()))


class SendMessage(APIView):
    """
    This is a sample api to send a message.
    """

    def post(self, request):
        peer_id = -488152794  # TODO: Is this a constant?
        future = send_msg(peer_id, request.data)
        return HttpResponse(get_event_loop().run_until_complete(future))


class Dialog(APIView):
    """
    It is used to retrive dialogs(open conversations)
    """

    def get(self, request):
        loop = get_event_loop()
        return HttpResponse(loop.run_until_complete(get_dialogs()))


def get_event_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop
