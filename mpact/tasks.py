from celery import shared_task
from .services import send_msg
from .views import new_or_current_event_loop


@shared_task
def send_msgs(receiver_id, message):
    return new_or_current_event_loop().run_until_complete(
        send_msg(int(receiver_id), message)
    )
