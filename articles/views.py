from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import (Article, ArticleComment, ArticleVote, ArticleTag,
                     ArticleImage)
from .serializers import (ArticleImageSerializer, ArticleSerializer,
                          ArticleCommentSerializer, ArticleVoteSerializer,
                          ArticleTagSerializer)
from .permissions import IsArticleOwnerOrReadOnly
from profiles.permissions import IsOwnerOrReadOnly, IsAdminUserOrReadOnly


class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_url_kwarg = 'article_id'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ArticleCommentListView(generics.ListCreateAPIView):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return ArticleComment.objects.filter(
            article=article_id).order_by('-created_time')

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        article = get_object_or_404(Article, id=article_id)
        serializer.save(user=self.request.user, article=article)


class ArticleCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        article_id = self.kwargs.get('article_id')
        comment_id = self.kwargs.get('comment_id')
        return ArticleComment.objects.get(id=comment_id, article=article_id)


class ArticleImageListView(generics.ListCreateAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = [IsAuthenticated, IsArticleOwnerOrReadOnly]

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return ArticleImage.objects.filter(
            article=article_id).order_by('-created_time')

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        article = get_object_or_404(Article, id=article_id)
        serializer.save(article=article)


class ArticleImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = [IsAuthenticated, IsArticleOwnerOrReadOnly]

    def get_object(self):
        article_id = self.kwargs.get('article_id')
        image_id = self.kwargs.get('image_id')
        return ArticleImage.objects.get(id=image_id, article=article_id)


class ArticleVoteListView(generics.ListCreateAPIView):
    queryset = ArticleVote.objects.all()
    serializer_class = ArticleVoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return ArticleVote.objects.filter(
            article=article_id).order_by('-created_time')

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        article = get_object_or_404(Article, id=article_id)
        serializer.save(user=self.request.user, article=article)


class ArticleVoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleVote.objects.all()
    serializer_class = ArticleVoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        article_id = self.kwargs.get('article_id')
        vote_id = self.kwargs.get('vote_id')
        return ArticleVote.objects.get(id=vote_id, article=article_id)


class ArticleTagListView(generics.ListCreateAPIView):
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer
    permission_classes = [IsAuthenticated]


class ArticleTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleTag.objects.all()
    serializer_class = ArticleTagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_url_kwarg = 'tag_id'
