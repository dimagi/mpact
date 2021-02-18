import os
from rest_framework import status


CHAT_ID = "chat_id"
CODE = "code"
PHONE = "phone"
MESSAGE = "message"
LOGOUT = "Logout successful"
MESSAGE_SENT = "Message sent"
INVALID_CODE = "Invalid code"
PASSWORD_REQUIRED = "Password required"
PASSWORD = "password"
PHONE_CODE_HASH = "phone_code_hash"
PHONE_NOT_REGISTERED = "Phone number is not registered in our system."
STATUS = "status"
DATA = "data"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
USERNAME = "username"
TWO_FA_ENABLED = "is_2FA_enabled"
IS_SUCCESS = "is_success"
INDIVIDUAL = "individual"
TOKEN = "token"
FLAGGED_MESSAGE = "flagged_messages"
ID = "id"

DIALOGS_LIMIT = 25

# Environment Variables
TELEGRAM_API_ID = os.environ["TELEGRAM_API_ID"]
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
SECURED_URL_SECRET_KEY = os.environ.get("SECURED_URL_SECRET_KEY")
SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")


# Responses
NOT_AUTHORIZED = {
    DATA: {MESSAGE: "Not authorized", IS_SUCCESS: False},
    STATUS: status.HTTP_401_UNAUTHORIZED,
}

RECORD_NF = "Record not found"
DELETE_SUCCESS = "Delete successful"
DELETE_FAIL = "Delete fail"
GROUP_MSGS_FORBIDDEN = "Cannot fetch the message."
