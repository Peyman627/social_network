from rest_framework import generics

from .models import (Article, ArticleComment, ArticleVote, ArticleTag,
                     ArticleImage)
from .serializers import (ArticleSerializer, ArticleCommentSerializer,
                          ArticleVoteSerializer, ArticleTagSerializer)


class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_url_kwarg = 'article_id'
    permission_classes = []