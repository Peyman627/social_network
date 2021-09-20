from rest_framework import generics

from .models import (Article, ArticleComment, ArticleVote, ArticleTag,
                     ArticleImage)
from .serializers import (ArticleSerializer, ArticleCommentSerializer,
                          ArticleVoteSerializer, ArticleTagSerializer)


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = []
