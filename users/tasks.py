from celery import shared_task
from celery.utils.log import get_task_logger

from .utils import Util
from .models import PhoneToken

logger = get_task_logger(__name__)


@shared_task
def send_verify_email_task(email_data):
    logger.info('sent verification email')
    Util.send_email(email_data)


@shared_task
def send_password_reset_email_task(email_data):
    logger.info('sent password reset email')
    Util.send_email(email_data)


@shared_task
def send_otp_sms_task(sms_data):
    logger.info('sent otp sms')
    Util.send_sms(sms_data)


@shared_task(name='users.tasks.delete_used_phone_tokens_task')
def delete_used_phone_tokens_task():
    logger.info('deleted used phone tokens')
    PhoneToken.objects.filter(used=True).delete()
