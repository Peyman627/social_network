from rest_framework import serializers
from rest_framework.reverse import reverse


class ArticleCommentHyperlinkedIdentityField(
        serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {'article_id': obj.article.id, 'comment_id': obj.id}
        return reverse(view_name,
                       kwargs=url_kwargs,
                       request=request,
                       format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'article': view_kwargs['article_id'],
            'id': view_kwargs['comment_id']
        }
        return self.get_queryset().get(**lookup_kwargs)


class ArticleImageHyperlinkedIdentityField(serializers.HyperlinkedIdentityField
                                           ):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {'article_id': obj.article.id, 'image_id': obj.id}
        return reverse(view_name,
                       kwargs=url_kwargs,
                       request=request,
                       format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'article': view_kwargs['article_id'],
            'id': view_kwargs['image_id']
        }
        return self.get_queryset().get(**lookup_kwargs)


class ArticleVoteHyperlinkedIdentityField(serializers.HyperlinkedIdentityField
                                          ):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {'article_id': obj.article.id, 'vote_id': obj.id}
        return reverse(view_name,
                       kwargs=url_kwargs,
                       request=request,
                       format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'article': view_kwargs['article_id'],
            'id': view_kwargs['vote_id']
        }
        return self.get_queryset().get(**lookup_kwargs)
