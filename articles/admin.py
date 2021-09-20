from django.contrib import admin

from .models import (Article, ArticleComment, ArticleImage, ArticleTag,
                     ArticleVote)


class ArticleCommentInline(admin.TabularInline):
    model = ArticleComment
    extra = 1


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


class ArticleVoteInline(admin.TabularInline):
    model = ArticleVote
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'created_time', 'updated_time')
    list_display_links = ('username', )
    date_hierarchy = 'created_time'
    inlines = (ArticleCommentInline, ArticleImageInline, ArticleVoteInline)

    @admin.display
    def username(self, obj):
        return obj.user.username


admin.site.register(ArticleComment)
admin.site.register(ArticleImage)
admin.site.register(ArticleVote)
