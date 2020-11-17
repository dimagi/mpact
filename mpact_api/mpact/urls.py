from django.urls import path

from . import views

urlpatterns = [
    path("listen_msg", views.ListenMessages.as_view(), name="listen_msg"),
]
