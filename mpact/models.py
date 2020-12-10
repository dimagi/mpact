from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


def validate_phone(username):
    if username[0] != "+":
        raise ValidationError("Phone number should start with '+'.")
    return username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number is invalid.",
    )
    phone = models.CharField(max_length=20, validators=[phone_regex, validate_phone])
