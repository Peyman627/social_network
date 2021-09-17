from django.contrib import admin

from .models import (Article, ArticleComment, ArticleImage, ArticleTag,
                     ArticleVote)

admin.site.register(Article)
admin.site.register(ArticleComment)
admin.site.register(ArticleImage)
admin.site.register(ArticleTag)
admin.site.register(ArticleVote)
