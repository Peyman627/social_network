from rest_framework import serializers

from .models import (Article, ArticleComment, ArticleTag, ArticleVote,
                     ArticleImage)
from profiles.serializer_fields import UserHyperlinkedRelatedField


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='articles:article_detail',
        lookup_url_kwarg='article_id',
    )
    user = UserHyperlinkedRelatedField(read_only=True)
    tags = serializers.SlugRelatedField(many=True,
                                        queryset=ArticleTag.objects.all(),
                                        slug_field='name')

    class Meta:
        model = Article
        fields = [
            'url', 'user', 'title', 'content', 'tags', 'created_time',
            'updated_time'
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
