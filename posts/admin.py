from django.contrib import admin

from .models import Post, PostLike


class PostLikeInline(admin.TabularInline):
    model = PostLike
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('parent', 'username', 'content', 'created_time')
    list_display_links = ('username', )
    date_hierarchy = 'created_time'
    inlines = (PostLikeInline, )

    @admin.display
    def username(self, obj):
        return obj.user.username


admin.site.register(PostLike)
