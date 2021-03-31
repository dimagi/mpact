import os

MESSAGE = "message"
MESSAGE_SENT = "Message sent"
STATUS = "status"
DATA = "data"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
USERNAME = "username"
IS_SUCCESS = "is_success"
TOKEN = "token"
FLAGGED_MESSAGE = "flagged_messages"
ID = "id"
WEBSOCKET_ROOM_NAME = "chat"
SENDER_ID = "sender_id"
SENDER_NAME = "sender_name"
FROM_GROUP = "from_group"
ROOM_ID = "room_id"
TELEGRAM_MSG_ID = "telegram_msg_id"

# Environment Variables
TELEGRAM_API_ID = os.environ["TELEGRAM_API_ID"]
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Responses
RECORD_NF = "Record not found"
DELETE_SUCCESS = "Delete successful"
DELETE_FAIL = "Delete fail"
FAIL_MSG = "Something went wrong"
EDIT_FAIL = "Message cannot be edited"
LOGOUT_SUCCESS = "Logout successful"

# Messages to beneficiaries/consumers
MSG_WELCOME = "Welcome!"
