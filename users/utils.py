from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.exceptions import APIException as RestAPIException
from kavenegar import KavenegarAPI, APIException, HTTPException


class Util:
    @staticmethod
    def send_email(data):
        subject = data['subject']
        body = data['body']
        to = data['to']
        email = EmailMessage(subject=subject, body=body, to=[to])
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
            raise RestAPIException('There was a problem!')

        except HTTPException:
            raise RestAPIException('Try again, an error occured')
