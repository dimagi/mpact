import os

CHAT_ID = "chat_id"
CODE = "code"
PHONE = "phone"
MESSAGE = "message"
LOGOUT = "Logout successful"
MESSAGE_SENT = "Message sent"
NOT_AUTHORIZED = "Not Authorized"
INVALID_CODE = "Invalid code"
PASSWORD_REQUIRED = "Password required"
PASSWORD = "password"
PHONE_CODE_HASH = "phone_code_hash"
PHONE_NOT_REGISTERED = "Phone number is not registered in our system."

# Environment Variables
TELEGRAM_API_ID = os.environ["TELEGRAM_API_ID"]
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
