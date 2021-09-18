from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=128, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'created_time', 'updated_time']
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'email': {
                'read_only': True
            }
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
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

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.name = validated_data.get('name', instance.name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        user.phone = user_data.get('phone', user.phone)
        user.save()

        return instance
