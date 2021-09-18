from django.db.models import fields
from rest_framework import serializers

from .models import Profile
from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField(read_only=True)
    followings_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user', 'name', 'bio', 'followers_count', 'followings_count',
            'followers', 'created_time', 'updated_time'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.user.followings.count()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone', 'is_verified', 'is_active',
            'is_staff', 'created_time', 'updated_time'
        ]
