from django.urls import path

from . import views

urlpatterns = [
    path("set_webhook", views.Webhook.as_view()),
    path("listen_msg", views.ListenMessages.as_view(), name="listen_msg"),
]
