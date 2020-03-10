from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Post, Comment,PostLike

class PostAdmin(ModelAdmin):
    list_display = ["title", "created_date", "author"]
    search_fields = ["title", "text", "author"]
    list_filter = ["created_date", "author"]
admin.site.register(Post, PostAdmin)

admin.site.register(Comment)


class PostLikeAdmin(ModelAdmin):
    list_display = ["post", "liked_by"]
    search_fields = ["post", "liked_by"]
    list_filter = ["cr_date"]
admin.site.register(PostLike, PostLikeAdmin)
