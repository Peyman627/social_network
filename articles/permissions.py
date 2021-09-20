from rest_framework import permissions

from .models import Article


class IsArticleOwnerOrReadOnly(permissions.BasePermission):
    message = 'access not allowed'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            article = Article.objects.get(
                pk=request.parser_context["kwargs"]["article_id"])
        except Article.DoesNotExist:
            return False
        return article.user == request.user

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.article.user == request.user
