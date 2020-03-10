from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Profile,FollowUser

class FollowUserAdmin(ModelAdmin):
    list_display = ["profile", "followed_by"]
    search_fields = ["profile", "followed_by"]
    list_filter = ["profile", "followed_by"]
admin.site.register(FollowUser, FollowUserAdmin)


class ProfileAdmin(ModelAdmin):
    list_display = ["user","gender","phone_no"]
    search_fields = ["user", "status", "phone_no"]
    list_filter = ["status", "gender"]
admin.site.register(Profile, ProfileAdmin)
