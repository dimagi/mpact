import asyncio

from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

import tablib
from telegram_bot.constants import (
    DATA,
    FAIL_MSG,
    IS_SUCCESS,
    LOGOUT_SUCCESS,
    MESSAGE,
    STATUS,
)
from telegram_bot.logger import logger

from .csv_serializer import Serializer as CSVSerializer
from .models import GroupChat, Message
from .serializers import CustomTokenObtainPairSerializer
from .services import (
    create_flagged_message,
    delete_flagged_message,
    edit_message,
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
        room_id = int(data['room_id'])
        message = data['message']
        result = new_or_current_event_loop().run_until_complete(send_msg(room_id, message))
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
    It is used to retrieve dialogs (open conversations)
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
        """
        Returns the scheduled messages file with a sheet for each group chat
        and any messages that have been scheduled for that chat.
        """
        if not GroupChat.objects.exists():
            return Response({
                'message': 'You must create a group chat before uploading a message schedule.',
            }, status=400)

        headers = ["Days", "Message", "Comment"]
        databook = tablib.Databook()
        for group in GroupChat.objects.all():
            sheet = tablib.Dataset(headers=headers)
            # excel limits titles to 32 characters: https://github.com/dimagi/mpact/issues/34
            sheet.title = f"{group.title[:22]}|{group.id}"
            for message in group.scheduled_messages.filter(enabled=True):
                sheet.append((message.day, message.message, message.comment))
            databook.add_sheet(sheet)

        xlsx = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(databook.export("xlsx"), content_type=xlsx)
        response['Content-Disposition'] = 'attachment; filename="schedules.xlsx"'
        return response

    def post(self, request):
        file = request.data["file"]
        result = schedule_messages(file)
        return Response(result[DATA], status=result[STATUS])


class StudyParticipants(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Returns an empty study participants file with a columns
        for study id and phone number
        """
        headers = ["Study ID", "Phone Number"]
        databook = tablib.Databook()
        sheet = tablib.Dataset(headers=headers)
        sheet.title = "Study Particpants"
        databook.add_sheet(sheet)
        xlsx = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(databook.export("xlsx"), content_type=xlsx)
        response['Content-Disposition'] = 'attachment; filename="study-participants.xlsx"'
        return response

    def post(self, request):
        # todo
        raise Exception('post not suppoted')

class ExportMessages(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        csv_serializer = CSVSerializer()
        response = HttpResponse(content_type="text/csv")

        csv_serializer.serialize(Message.objects.all(), stream=response, fields=(
            'telegram_msg_id',
            'sender_id',
            'sender_name',
            'room_id',
            'message',
            'date',
            'from_group',
            'is_flagged',
        ))
        response['Content-Disposition'] = 'attachment; filename="messages.csv"'
        return response


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


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {MESSAGE: LOGOUT_SUCCESS, IS_SUCCESS: True},
                status=status.HTTP_200_OK,
            )
        except Exception as exception:
            logger.exception(exception)
            return Response(
                {MESSAGE: FAIL_MSG, IS_SUCCESS: False},
                status=status.HTTP_400_BAD_REQUEST,
            )
