from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.exceptions import APIException as RestAPIException
from kavenegar import KavenegarAPI, APIException, HTTPException


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(**data)
        email.send()

    @staticmethod
    def send_sms(data):
        api_key = settings.KAVENEGAR_API_KEY
        receptor = data['receptor']
        message = data['message']
        try:
            api = KavenegarAPI(api_key)
            params = {
                'sender': '10004346',
                'receptor': receptor,
                'message': message
            }
            api.sms_send(params)

        except APIException:
            raise RestAPIException(
                'Service temporarily unavailable, try again later.', code=503)

        except HTTPException:
            raise RestAPIException('Try again, an error occurred', code=400)
