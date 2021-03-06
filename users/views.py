import jwt

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (RegisterSerializer, EmailVerificationSerializer,
                          LoginSerializer, PasswordResetSerializer,
                          SetNewPasswordSerializer, LogoutSerializer,
                          PhoneTokenCreateSerializer,
                          PhoneTokenValidateSerializer)
from .models import PhoneToken
from .tasks import send_verify_email_task, send_otp_sms_task

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user).access_token

        address = reverse('users:email_verify', request=request)
        verify_url = f'{address}?token={token}'

        email_body = f'Hi {user.username}. Please use the link below to verify your email\n{verify_url}'
        email_data = {
            'subject': 'Verify your email',
            'body': email_body,
            'to': [user.email]
        }

        send_verify_email_task.apply_async((email_data,))

        return Response(
            {
                'success': 'Successfully created',
                'detail': 'Verify account using the sent email'
            },
            status=status.HTTP_201_CREATED)


class EmailVerifyView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token,
                                 settings.SECRET_KEY,
                                 algorithms=['HS256'])

            user = User.objects.get(pk=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'success': "Successfully activated"},
                            status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation expired'},
                            status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK)


class PasswordTokenCheckView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token is not valid, please request a new one'},
                    status=status.HTTP_401_UNAUTHORIZED)

            return Response(
                {
                    'success': 'Credentials valid',
                    'uidb64': uidb64,
                    'token': token
                },
                status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response(
                {'error': 'Token is not valid, please request a new one'},
                status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'success': 'Password reset complete'},
                        status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GenerateOTPView(generics.CreateAPIView):
    queryset = PhoneToken.objects.all()
    serializer_class = PhoneTokenCreateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            number = request.data.get('phone')
            token, otp = PhoneToken.create_otp_for_number(number)

            sms_data = {
                'receptor': number,
                'message': f'Your code for login: {otp}'
            }
            send_otp_sms_task.apply_async((sms_data,))

            if token:
                phone_token = self.serializer_class(
                    token, context={'request': request})
                data = phone_token.data

                if getattr(settings, 'PHONE_LOGIN_DEBUG', False):
                    data['debug_mode_token'] = token.otp

                return Response(data)
            return Response(
                {
                    'reason':
                        "you can not have more than {n} attempts per day, please try again tomorrow".format(
                            n=getattr(settings, 'PHONE_LOGIN_ATTEMPTS', 10))
                },
                status=status.HTTP_403_FORBIDDEN)
        return Response({'reason': serializer.errors},
                        status=status.HTTP_406_NOT_ACCEPTABLE)


class ValidateOTPView(generics.CreateAPIView):
    queryset = PhoneToken.objects.all()
    serializer_class = PhoneTokenValidateSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            pk = request.data.get("pk")
            otp = request.data.get("otp")
            try:
                user = authenticate(request, pk=pk, otp=otp)
                user_data = {
                    'username': user.username,
                    'tokens': user.tokens()
                }
                return Response(user_data, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return Response({'reason': "OTP doesn't exist"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response({'reason': serializer.errors},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
