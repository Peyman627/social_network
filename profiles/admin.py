from django.contrib import admin

from .models import Profile, FollowerRelation


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'created_time', 'updated_time')
    list_display_links = ('username', )
    date_hierarchy = 'created_time'

    @admin.display
    def username(self, obj):
        return obj.user.username


admin.site.register(FollowerRelation)
