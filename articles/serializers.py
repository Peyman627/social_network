from django.db.models import fields
from rest_framework import serializers

from .models import (Article, ArticleComment, ArticleTag, ArticleVote,
                     ArticleImage)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = '__all__'


class ArticleVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleVote
        fields = '__all__'


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = '__all__'


class ArticleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleTag
        fields = '__all__'
