from django.urls import path

from .views import Dialog, Login, Logout, SendMessage

urlpatterns = [
    path("login", Login.as_view()),
    path("logout", Logout.as_view()),
    path("send", SendMessage.as_view()),
    path("dialogs", Dialog.as_view()),
]
