from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("mpact.urls")),
    path("login/", TemplateView.as_view(template_name="index.html")),
    path("chat/", TemplateView.as_view(template_name="index.html")),
    path("flagged-messages/", TemplateView.as_view(template_name="index.html")),
    path("", TemplateView.as_view(template_name="index.html")),
]
