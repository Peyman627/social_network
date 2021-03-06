from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from .models import Profile, FollowRelation
from .serializer_fields import (UserHyperlinkedRelatedField,
                                FollowerRelationHyperlinkedRelatedField,
                                FollowingRelationHyperlinkedRelatedField)

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
    following_status = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    followings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user', 'name', 'bio', 'followers', 'followings',
            'followers_count', 'followings_count', 'following_status',
            'created_time', 'updated_time'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.user.followings.count()

    def get_following_status(self, obj):
        user = self.context.get('request').user
        return user in obj.followers.all()

    def get_followers(self, obj):
        request = self.context.get('request')
        return reverse(viewname='profiles:follower_relation_list',
                       args=[obj.id],
                       request=request)

    def get_followings(self, obj):
        request = self.context.get('request')
        return reverse(viewname='profiles:following_relation_list',
                       args=[obj.id],
                       request=request)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.name = validated_data.get('name', instance.name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        user.phone = user_data.get('phone', user.phone)
        user.save()

        return instance


class FollowerRelationSerializer(serializers.HyperlinkedModelSerializer):
    url = FollowerRelationHyperlinkedRelatedField(source='*', read_only=True)
    user = UserHyperlinkedRelatedField(read_only=True)
    profile = serializers.HyperlinkedRelatedField(
        view_name='profiles:profile_detail',
        lookup_url_kwarg='profile_id',
        read_only=True)

    class Meta:
        model = FollowRelation
        fields = ['url', 'user', 'profile', 'created_time']


class FollowingRelationSerializer(serializers.HyperlinkedModelSerializer):
    url = FollowingRelationHyperlinkedRelatedField(source='*', read_only=True)
    user = UserHyperlinkedRelatedField(read_only=True)
    profile = serializers.HyperlinkedRelatedField(
        view_name='profiles:profile_detail',
        lookup_url_kwarg='profile_id',
        read_only=True)

    class Meta:
        model = FollowRelation
        fields = ['url', 'user', 'profile', 'created_time']
