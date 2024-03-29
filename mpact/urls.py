from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    CustomTokenObtainPairView,
    Dialog,
    FlagMessage,
    FlagMessageDelete,
    GetMessages,
    IndividualDetails,
    Logout,
    ScheduleMessages,
    StudyParticipants,
    SendMessage,
    ExportMessages,
)

urlpatterns = [
    path("messages", SendMessage.as_view()),
    path("messages/<int:room_id>", GetMessages.as_view()),
    path("dialogs", Dialog.as_view()),
    path("flaggedmessages", FlagMessage.as_view()),
    path("flaggedmessages/<int:id>", FlagMessageDelete.as_view()),
    path("schedule_messages", ScheduleMessages.as_view()),
    path("schedules.xlsx", ScheduleMessages.as_view()),
    path("study_participants.xlsx", StudyParticipants.as_view()),
    path("messages.csv", ExportMessages.as_view()),
    path("individuals/<int:individual_id>", IndividualDetails.as_view()),

    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),

    path('logout', Logout.as_view()),
]
