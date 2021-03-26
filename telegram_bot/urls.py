from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from mpact.views import CustomTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("mpact.urls")),
    path("login/", TemplateView.as_view(template_name="index.html")),
    path("chat/", TemplateView.as_view(template_name="index.html")),
    path("flagged-messages/", TemplateView.as_view(template_name="index.html")),
    path("", TemplateView.as_view(template_name="index.html")),
    # jwt token urls
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
]
