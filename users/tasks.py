from celery import shared_task
from celery.utils.log import get_task_logger

from .utils import Util

logger = get_task_logger(__name__)


@shared_task
def send_verify_email_task(email_data):
    logger.info('sent verification email')
    Util.send_email(email_data)
