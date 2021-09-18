from rest_framework import serializers
from rest_framework.reverse import reverse


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
