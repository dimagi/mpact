from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    Dialog,
    ExportMessages,
    FlagMessage,
    FlagMessageDelete,
    GetMessages,
    IndividualDetails,
    ScheduleMessages,
    SendMessage,
    Logout,
)
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("messages", SendMessage.as_view()),
    path("messages/<int:room_id>", GetMessages.as_view()),
    path("dialogs", Dialog.as_view()),
    path("flaggedmessages", FlagMessage.as_view()),
    path("flaggedmessages/<int:id>", FlagMessageDelete.as_view()),
    path("schedule_messages", ScheduleMessages.as_view()),
    path("export_messages", ExportMessages.as_view()),
    path("individuals/<int:individual_id>", IndividualDetails.as_view()),

    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),

    path('logout', Logout.as_view()),
]
