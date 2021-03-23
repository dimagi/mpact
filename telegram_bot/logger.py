import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - p%(process)s {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)