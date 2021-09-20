from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import (Article, ArticleComment, ArticleTag, ArticleVote,
                     ArticleImage)
from profiles.serializer_fields import UserHyperlinkedRelatedField
from .serializer_fields import (ArticleCommentHyperlinkedIdentityField,
                                ArticleVoteHyperlinkedIdentityField,
                                ArticleImageHyperlinkedIdentityField)


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
    votes = serializers.SerializerMethodField(read_only=True)
    votes_average = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'url', 'user', 'title', 'content', 'images', 'comments', 'votes',
            'votes_average', 'tags', 'created_time', 'updated_time'
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

    def get_votes(self, obj):
        request = self.context.get('request')
        return reverse(viewname='articles:vote_list',
                       args=[obj.id],
                       request=request)

    def get_votes_average(self, obj):
        votes_count = obj.votes.count()
        if votes_count != 0:
            votes_total = sum([vote.value for vote in obj.votes.all()])
            return votes_total / votes_count
        return 0


class ArticleCommentSerializer(serializers.HyperlinkedModelSerializer):
    url = ArticleCommentHyperlinkedIdentityField(
        view_name='articles:comment_detail')
    article = serializers.HyperlinkedRelatedField(
        view_name='articles:article_detail',
        lookup_url_kwarg='article_id',
        read_only=True)
    user = UserHyperlinkedRelatedField(read_only=True)

    class Meta:
        model = ArticleComment
        fields = [
            'url', 'article', 'user', 'content', 'created_time', 'updated_time'
        ]


class ArticleVoteSerializer(serializers.ModelSerializer):
    url = ArticleVoteHyperlinkedIdentityField(view_name='articles:vote_detail')
    user = UserHyperlinkedRelatedField(read_only=True)
    article = serializers.HyperlinkedRelatedField(
        view_name='articles:article_detail',
        lookup_url_kwarg='article_id',
        read_only=True)

    class Meta:
        model = ArticleVote
        fields = ['url', 'user', 'article', 'value', 'created_time']
        extra_kwargs = {
            'value': {
                'min_value': 1,
                'max_value': 10
            },
        }


class ArticleImageSerializer(serializers.ModelSerializer):
    url = ArticleImageHyperlinkedIdentityField(
        view_name='articles:image_detail')
    article = serializers.HyperlinkedRelatedField(
        view_name='articles:article_detail',
        lookup_url_kwarg='article_id',
        read_only=True)

    class Meta:
        model = ArticleImage
        fields = ['url', 'name', 'article', 'image', 'created_time']


class ArticleTagSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='articles:tag_detail',
                                               lookup_url_kwarg='tag_id')

    class Meta:
        model = ArticleTag
        fields = ['url', 'name']
