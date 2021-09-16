from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6,
                                     max_length=70,
                                     write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contain alphanumeric characters')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=4,
                                   max_length=255,
                                   required=False)
    phone = serializers.CharField(max_length=128, required=False)
    password = serializers.CharField(min_length=6,
                                     max_length=60,
                                     write_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'username', 'tokens']

    def get_tokens(self, obj):
        email = obj.get('email', '')
        phone = obj.get('phone', '')

        try:
            user = User.objects.get(Q(email=email) | Q(phone=phone))
            return user.tokens()

        except User.DoesNotExist:
            return None

    def get_username(self, obj):
        email = obj.get('email', '')
        phone = obj.get('phone', '')

        try:
            user = User.objects.get(Q(email=email) | Q(phone=phone))
            return user.username

        except User.DoesNotExist:
            return None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        phone = attrs.get('phone')

        user = authenticate(email=email, phone=phone, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return attrs
