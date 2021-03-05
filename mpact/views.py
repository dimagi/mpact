import asyncio

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from telegram_bot.constants import DATA, STATUS

from mpact.serializers import CustomTokenObtainPairSerializer
from mpact.services import (
    create_flagged_message,
    delete_flagged_message,
    download_schedule_messages_file,
    edit_message,
    export_messages,
    get_dialog,
    get_flagged_messages,
    get_individual_details,
    get_messages,
    schedule_messages,
    send_msg,
    update_individual_details,
)


def new_or_current_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


class SendMessage(APIView):
    """
    This is a sample api to send a message.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(send_msg(data))
        return Response(result[DATA], status=result[STATUS])


class GetMessages(APIView):
    """
    returns the messages.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, room_id):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        user_id = request.user.id

        result = new_or_current_event_loop().run_until_complete(
            get_messages(room_id, user_id, limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])

    def put(self, request, room_id):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(
            edit_message(room_id, data)
        )
        return Response(result[DATA], status=result[STATUS])


class Dialog(APIView):
    """
    It is used to retrive dialogs(open conversations)
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        result = new_or_current_event_loop().run_until_complete(get_dialog(user_id))
        return Response(result[DATA], status=result[STATUS])


class FlagMessage(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        result = new_or_current_event_loop().run_until_complete(
            get_flagged_messages(limit, offset)
        )
        return Response(result[DATA], status=result[STATUS])

    def post(self, request):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(
            create_flagged_message(data)
        )
        return Response(result[DATA], status=result[STATUS])


class FlagMessageDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id):
        result = new_or_current_event_loop().run_until_complete(
            delete_flagged_message(id)
        )
        return Response(result[DATA], status=result[STATUS])


class ScheduleMessages(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        result = new_or_current_event_loop().run_until_complete(
            download_schedule_messages_file()
        )
        return Response(result[DATA], status=result[STATUS])

    def post(self, request):
        file = request.data["file"]
        result = new_or_current_event_loop().run_until_complete(schedule_messages(file))
        return Response(result[DATA], status=result[STATUS])


class ExportMessages(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        result = new_or_current_event_loop().run_until_complete(export_messages())
        return Response(result[DATA], status=result[STATUS])


class IndividualDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, individual_id):
        result = new_or_current_event_loop().run_until_complete(
            get_individual_details(individual_id)
        )
        return Response(result[DATA], status=result[STATUS])

    def put(self, request, individual_id):
        data = request.data
        result = new_or_current_event_loop().run_until_complete(
            update_individual_details(individual_id, data)
        )
        return Response(result[DATA], status=result[STATUS])


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
