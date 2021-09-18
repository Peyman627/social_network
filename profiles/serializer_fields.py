from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

User = get_user_model()


class FollowerRelationHyperlinkedRelatedField(
        serializers.HyperlinkedRelatedField):
    view_name = 'profiles:follower_relation_detail'

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


class FollowingRelationHyperlinkedRelatedField(
        serializers.HyperlinkedRelatedField):
    view_name = 'profiles:following_relation_detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {'profile_id': obj.user.profile.id, 'follow_id': obj.id}
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