# pylint: disable=missing-module-docstring
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # pylint: disable=too-few-public-methods
    """User Class, defines properties of User model in Django"""
    first_name:models.CharField = models.CharField(max_length=50, blank=True)
    last_name:models.CharField = models.CharField(max_length=50, blank=True)
    email:models.EmailField = models.EmailField()
    created_at:models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at:models.DateTimeField = models.DateTimeField(auto_now=True)
    can_post:models.BooleanField = models.BooleanField(default=False)
    can_comment:models.BooleanField = models.BooleanField(default=True)

    def __str__(self) -> str:
        if self.first_name == "" and self.last_name == "":
            return self.username
        return self.first_name + " " + self.last_name



class Post(models.Model):
    # pylint: disable=too-few-public-methods
    """Post Class, defines properties of Post model in Django"""
    class Meta:
        """Tells Django to label it as 'Posts' in Admin interface"""
        verbose_name_plural = "Posts"

    title:models.CharField = models.CharField(max_length=100)
    created_at:models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at:models.DateTimeField = models.DateTimeField(auto_now=True)
    author:models.ForeignKey = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    post_content:models.CharField = models.CharField(max_length=20000)



class Comment(models.Model):
    # pylint: disable=too-few-public-methods
    """Comment Class, defines properties of Comment model in Django"""
    class Meta:
        """Tells Django to label it as 'Comments' in Admin interface"""
        verbose_name_plural = "Comments"

    commenter:models.ForeignKey = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    created_at:models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at:models.DateTimeField = models.DateTimeField(auto_now=True)
    post:models.ForeignKey = models.ForeignKey(
        "Post",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    comment_content:models.CharField = models.CharField(max_length=1000)
