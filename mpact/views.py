import asyncio

from constants import DATA, STATUS
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import token_required

from mpact.services import (
    create_flagged_message,
    delete_flagged_message,
    get_chat_msg,
    get_dialog,
    get_flagged_messages,
    get_individual_msg,
    login,
    logout,
    send_msg,
)


def new_or_current_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


class Login(APIView):
    """
    It is used to login into telegram
    """

    def post(self, request):
        # request.data will contain phone or code.
        data = request.data
        result = new_or_current_event_loop().run_until_complete(login(data))
        return Response(result[DATA], status=result[STATUS])


class Logout(APIView):
    """
    It is used to log out from telegram.
    """

    @token_required
    def get(self, request, phone):
        result = new_or_current_event_loop().run_until_complete(logout(phone))
        return Response(result[DATA], status=result[STATUS])


class SendMessage(APIView):
    """
    This is a sample api to send a message.
    """

    @token_required
    def post(self, request, phone):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(send_msg(phone, data))
        return Response(result[DATA], status=result[STATUS])


class GetIndividaulMessage(APIView):
    """
    returns the individual messages.
    """

    @token_required
    def get(self, request, phone, individual_id):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        result = new_or_current_event_loop().run_until_complete(
            get_individual_msg(phone, individual_id, limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])


class GetChatMessage(APIView):
    """
    returns the chat messages.
    """

    @token_required
    def get(self, request, phone, chat_id):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        result = new_or_current_event_loop().run_until_complete(
            get_chat_msg(phone, chat_id, limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])


class Dialog(APIView):
    """
    It is used to retrive dialogs(open conversations)
    """

    @token_required
    def get(self, request, phone):
        result = new_or_current_event_loop().run_until_complete(get_dialog(phone))
        return Response(result[DATA], status=result[STATUS])


class FlagMessage(APIView):
    @token_required
    def get(self, request, phone):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        result = new_or_current_event_loop().run_until_complete(
            get_flagged_messages(phone, limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])

    @token_required
    def post(self, request, phone):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(
            create_flagged_message(phone, data)
        )
        return Response(result[DATA], status=result[STATUS])


class FlagMessageDelete(APIView):
    @token_required
    def delete(self, request, phone, id):
        result = new_or_current_event_loop().run_until_complete(
            delete_flagged_message(phone, id)
        )
        return Response(result[DATA], status=result[STATUS])
