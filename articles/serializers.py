from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import (Article, ArticleComment, ArticleTag, ArticleVote,
                     ArticleImage)
from profiles.serializer_fields import UserHyperlinkedRelatedField


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='articles:article_detail',
        lookup_url_kwarg='article_id',
    )
    user = UserHyperlinkedRelatedField(read_only=True)
    tags = serializers.SlugRelatedField(queryset=ArticleTag.objects.all(),
                                        many=True,
                                        slug_field='name')
    comments = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'url', 'user', 'title', 'content', 'images', 'tags', 'comments',
            'votes', 'created_time', 'updated_time'
        ]

    def get_comments(self, obj):
        request = self.context.get('request')
        return reverse(viewname='articles:comment_list',
                       args=[obj.id],
                       request=request)

    def get_images(self, obj):
        request = self.context.get('request')
        return reverse(viewname='articles:image_list',
                       args=[obj.id],
                       request=request)


class ArticleCommentSerializer(serializers.HyperlinkedModelSerializer):
    article = serializers.HyperlinkedRelatedField(
        view_name='articles:article_detail',
        lookup_url_kwarg='article_id',
        read_only=True)
    user = UserHyperlinkedRelatedField(read_only=True)

    class Meta:
        model = ArticleComment
        fields = ['article', 'user', 'content', 'created_time', 'updated_time']


class ArticleVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleVote
        fields = ['user', 'article', 'value', 'created_time']


class ArticleImageSerializer(serializers.ModelSerializer):
    article = serializers.HyperlinkedRelatedField(
        view_name='articles:article_detail',
        lookup_url_kwarg='article_id',
        read_only=True)

    class Meta:
        model = ArticleImage
        fields = ['name', 'article', 'image', 'created_time']


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ['name']
