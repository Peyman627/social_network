from rest_framework import generics

from .models import (Article, ArticleComment, ArticleVote, ArticleTag,
                     ArticleImage)
from .serializers import (ArticleImageSerializer, ArticleSerializer,
                          ArticleCommentSerializer, ArticleVoteSerializer,
                          ArticleTagSerializer)


class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_url_kwarg = 'article_id'
    permission_classes = []


class ArticleCommentListView(generics.ListCreateAPIView):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = []

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return ArticleComment.objects.filter(
            article=article_id).order_by('-created_time')


class ArticleCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = []

    def get_object(self):
        article_id = self.kwargs.get('article_id')
        comment_id = self.kwargs.get('comment_id')
        return ArticleComment.objects.get(id=comment_id, article=article_id)


class ArticleImageListView(generics.ListCreateAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = []

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return ArticleImage.objects.filter(
            article=article_id).order_by('-created_time')


class ArticleImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = []

    def get_object(self):
        article_id = self.kwargs.get('article_id')
        image_id = self.kwargs.get('image_id')
        return ArticleImage.objects.get(id=image_id, article=article_id)


class ArticleVoteListView(generics.ListCreateAPIView):
    queryset = ArticleVote.objects.all()
    serializer_class = ArticleVoteSerializer
    permission_classes = []

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return ArticleVote.objects.filter(
            article=article_id).order_by('-created_time')


class ArticleVoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleVote.objects.all()
    serializer_class = ArticleVoteSerializer
    permission_classes = []

    def get_object(self):
        article_id = self.kwargs.get('article_id')
        vote_id = self.kwargs.get('vote_id')
        return ArticleVote.objects.get(id=vote_id, article=article_id)


class ArticleTagListView(generics.ListCreateAPIView):
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer
    permission_classes = []


class ArticleTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer
    permission_classes = []
