from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Post, PostLike
from profiles.serializers import UserHyperlinkedRelatedField


class PostLikeHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    view_name = 'posts:post_like_detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {'post_id': obj.post.id, 'like_id': obj.id}
        return reverse(view_name,
                       kwargs=url_kwargs,
                       request=request,
                       format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'post': view_kwargs['post_id'],
            'id': view_kwargs['like_id']
        }
        return self.get_queryset().get(**lookup_kwargs)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='posts:post_detail',
                                               lookup_url_kwarg='post_id',
                                               read_only=True)
    parent = serializers.HyperlinkedRelatedField(view_name='posts:post_detail',
                                                 lookup_url_kwarg='post_id',
                                                 read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user = UserHyperlinkedRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'url', 'parent', 'user', 'likes_count', 'content', 'image',
            'created_time'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()


class PostLikeSerializer(serializers.ModelSerializer):
    url = PostLikeHyperlinkedRelatedField(source='*', read_only=True)
    user = UserHyperlinkedRelatedField(read_only=True)
    post = serializers.HyperlinkedRelatedField(view_name='posts:post_detail',
                                               lookup_url_kwarg='post_id',
                                               read_only=True)

    class Meta:
        model = PostLike
        fields = ['url', 'user', 'post', 'created_time']
