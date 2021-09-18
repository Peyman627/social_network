from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from .models import Profile, FollowRelation

User = get_user_model()


class FollowRelationHyperlinkedRelatedField(serializers.HyperlinkedRelatedField
                                            ):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {'profile_id': obj.profile.id, 'follow_id': obj.id}
        return reverse(view_name,
                       kwargs=url_kwargs,
                       request=request,
                       format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'profile': view_kwargs['profile_id'],
            'id': view_kwargs['follow_id']
        }
        return self.get_queryset().get(**lookup_kwargs)


class UserHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    view_name = 'profiles:profile_detail'

    def get_url(self, obj, view_name, request, format):
        user = User.objects.get(pk=obj.pk)
        url_kwargs = {'profile_id': user.profile.id}
        return reverse(view_name,
                       kwargs=url_kwargs,
                       request=request,
                       format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'id': view_kwargs['profile_id'],
        }
        return self.get_queryset().get(**lookup_kwargs)


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
            'created_time', 'updated_time'
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


class FollowerRelationSerializer(serializers.HyperlinkedModelSerializer):
    url = FollowRelationHyperlinkedRelatedField(
        view_name='profiles:follower_relation_detail',
        source='*',
        read_only=True)
    user = UserHyperlinkedRelatedField(read_only=True)
    profile = serializers.HyperlinkedRelatedField(
        view_name='profiles:profile_detail',
        lookup_url_kwarg='profile_id',
        read_only=True)

    class Meta:
        model = FollowRelation
        fields = ['url', 'user', 'profile', 'created_time']


class FollowingRelationSerializer(serializers.HyperlinkedModelSerializer):
    url = FollowRelationHyperlinkedRelatedField(
        view_name='profiles:following_relation_detail',
        source='*',
        read_only=True)
    user = UserHyperlinkedRelatedField(read_only=True)
    profile = serializers.HyperlinkedRelatedField(
        view_name='profiles:profile_detail',
        lookup_url_kwarg='profile_id',
        read_only=True)

    class Meta:
        model = FollowRelation
        fields = ['url', 'user', 'profile', 'created_time']
