from django.urls import path
#from rest_framework import routers
from .views import  (comment_utils,
                     create_new_comment_on,
                     create_new_post,
                     create_new_user,
                     get_all_comments,
                     get_all_comments_by,
                     get_all_comments_on,
                     get_all_posts,
                     get_all_posts_by,
                     get_all_users,
                     post_utils,
                     user_utils)
                     

urlpatterns = [
    path('users/', get_all_users),
    path('users/<str:username>/posts/', get_all_posts_by),
    path('users/<str:username>/comments/', get_all_comments_by),
    path('users/new/', create_new_user),
    path('users/<int:pk>/', user_utils),

    path('posts/', get_all_posts),
    path('posts/usr=<str:username>/', get_all_posts_by),
    path('posts/<int:pk>/comments/', get_all_comments_on),
    path('posts/new/', create_new_post),
    path('posts/<int:pk>/', post_utils),
    
    path('comments/', get_all_comments),
    path('comments/usr=<str:username>/', get_all_comments_by),
    path('comments/post=<int:pk>/', get_all_comments_on),
    path('comments/post=<int:pk>/new/', create_new_comment_on),
    path('comments/<int:pk>/', comment_utils),
]
