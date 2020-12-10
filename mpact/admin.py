from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',),
        }),
    )
    inlines = (UserProfileInline, )
