from rest_framework import serializers

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

    class Meta:
        model = Article
        fields = [
            'url', 'user', 'title', 'content', 'images', 'tags', 'comments',
            'votes', 'created_time', 'updated_time'
        ]


class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['article', 'user', 'content', 'created_time', 'updated_time']


class ArticleVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleVote
        fields = ['user', 'article', 'value', 'created_time']


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['name', 'article', 'image', 'created_time']


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = ['name']
