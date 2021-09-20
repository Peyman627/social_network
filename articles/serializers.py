from rest_framework import serializers

from .models import (Article, ArticleComment, ArticleTag, ArticleVote,
                     ArticleImage)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'user', 'title', 'content', 'tags', 'created_time', 'updated_time'
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
