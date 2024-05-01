from django.contrib import admin
from .models import Comment, Post, User

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "date_joined", "last_login", "is_superuser")
    fields = ["id", "username", "first_name", "last_name", "email",
              "is_superuser",  "date_joined", "last_login", "groups",
              "user_permissions", "can_post", "can_comment", "is_staff", "is_active",]

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "updated_at")
    fields = ["id", "title", "author", "created_at", "updated_at", "post_content"]

class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "updated_at")
    fields = ["id", "commenter", "created_at", "updated_at", "post", "comment_content"]


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)