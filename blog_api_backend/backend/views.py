# pylint: disable=missing-module-docstring
from django.db.models.query import QuerySet
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from backend.models import User, Post, Comment
from backend.serializers import UserSerializer, PostSerializer, CommentSerializer



# USER ########################################################################################################
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_users(request:Request) -> Response:
    """Queries all User objects in Django's db and returns a JSON response containing them all.

    Args:
        request (rest_framework.request.Request): HTTP request method (GET)
    
    Return:
        Response: JSON data for all Users in Django's db
    """
    queryset:QuerySet = User.objects.all()
    serializer:UserSerializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_posts_by(request:Request, username: str) -> Response:
    """Queries all Post objects in Django's db provided a username (lists all blog posts done by a user)

    Args:
        request (rest_framework.request.Request): HTTP request method
        username (str): the username of the user we want to get all the posts for 
    
    Return:
        Response: JSON data for all Blog Posts in Django's db done by user
    """
    queryset_user:QuerySet = User.objects.get(username=username)
    queryset_posts:QuerySet = Post.objects.filter(author=queryset_user.id)
    serializer:PostSerializer = PostSerializer(queryset_posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_comments_by(request:Request, username: str) -> Response:
    """Queries all Comment objects in Django's db provided a username (lists all comments done by a user)

    Args:
        request (rest_framework.request.Request): HTTP request method (GET)
        username (str): the username of the user we want to get all the comments for 
    
    Return:
        Response: JSON data for all Comments in Django's db done by user
    """
    queryset_user:QuerySet = User.objects.get(username=username)
    queryset_comments:QuerySet = Comment.objects.filter(commenter=queryset_user.id)
    print(queryset_comments)
    serializer:CommentSerializer = CommentSerializer(queryset_comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_new_user(request:Request) -> Response:
    """Creates new User object and saves it to Django's db

    Args:
        request (rest_framework.request.Request): HTTP request methods (POST)
    
    Return:
        Response: JSON data confirming that HTTP POST was successful for the User
    """
    serializer:UserSerializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


def get_single_user(request:Request, pk:int):
    """Queries User objects in Django's db where the Users's id = the passed pk, Returns a JSON response containing
    data of that User.

    Args:
        request (rest_framework.request.Request): HTTP request methods (GET)
        pk (int): The id of the User in Django
    
    Return:
        Response: JSON data for User in Django's db, specified by pk/id
    """
    queryset:QuerySet = User.objects.filter(id=pk)
    serializer:UserSerializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


def put_single_user(request:Request, pk:int) -> Response:
    """Updates User object given the User's id.

    Args:
        request (rest_framework.request.Request): HTTP request methods (PUT)
        pk (int): The id of the User to update in Django
    
    Return:
        Response: JSON data confirming that HTTP PUT was successful for the Blog Post
    """
    try:
        serializer:UserSerializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=pk)
            user.username = serializer.data['username']
            user.first_name = serializer.data['first_name']
            user.last_name = serializer.data['last_name']
            user.can_post = serializer.data['can_post']
            user.can_comment = serializer.data['can_comment']
            user.save(force_update=True)
            return Response({"success": True, "user_id": user.id})
    except Exception as e:
        print (e)
        return Response({"success": False }, status = status.HTTP_400_BAD_REQUEST)


def delete_single_user(request:Request, pk:int) -> Response:
    """Deletes User object given the User's id.

    Args:
        request (rest_framework.request.Request): HTTP request methods (DELETE)
        pk (int): The id of the User to delete in Django
    
    Return:
        Response: JSON data confirming that HTTP Delete was successful for the User
    """
    try:
        user = User.objects.get(id=pk)
        deleted_id:int = user.id
        user.delete()
        return Response({"success": True, "comment_id": deleted_id})
    except Exception as e:
        print (e)
        return Response({"success": False }, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def user_utils(request:Request, pk: int) -> None:
    """Handles various HTTP methods (GET, PUT, or DELETE) that happen on /api/users/<int:pk>/.

    Args:
        request (rest_framework.request.Request): HTTP request methods (GET, PUT, or DELETE)
        pk (int): The id of the User to perform the HTTP method on in Django
    
    """
    match request.method:
        case 'GET':
            return get_single_user(request, pk)
        case 'PUT':
            return put_single_user(request, pk)
        case 'DELETE':
            return delete_single_user(request, pk)
        case _ :
            print('mmmmmm whoops something didnt go right')
###############################################################################################################



# POST ########################################################################################################
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_posts(request:Request) -> Response:
    """Queries all Post objects in Django's db and returns a JSON response containing them all.

    Args:
        request (rest_framework.request.Request): HTTP request method
    
    Return:
        Response: JSON data for all Blog Posts in Django's db
    """
    queryset:QuerySet = Post.objects.all()
    serializer:PostSerializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_comments_on(request:Request, pk:int) -> Response:
    """Queries all Comment objects in Django's db provided a post id (gets all comments on a particular post)

    Args:
        request (rest_framework.request.Request): HTTP request method (GET)
        pk (int): the id of the Post we want to get all the comments for 
    
    Return:
        Response: JSON data for all Comments in Django's db on a given Post
    """
    print(pk)
    queryset_post:QuerySet = Post.objects.get(id=pk)
    queryset_comments:QuerySet = Comment.objects.filter(post=queryset_post.id)
    serializer:CommentSerializer = CommentSerializer(queryset_comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_new_post(request:Request) -> Response:
    """Creates new Post object and saves it to Django's db

    Args:
        request (rest_framework.request.Request): HTTP request methods (POST)
    
    Return:
        Response: JSON data confirming that HTTP POST was successful for the Blog Post
    """
    serializer:PostSerializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "post_id": serializer.data['id']})
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


def get_single_blogpost(request:Request, pk:int):
    """Queries Post objects in Django's db where the Post's id = the passed pk, Returns a JSON response containing
    data of that blogpost.

    Args:
        request (rest_framework.request.Request): HTTP request methods
        pk (int): The id of the Blog Post in Django
    
    Return:
        Response: JSON data for Blog Post in Django's db, specified by pk/id
    """
    queryset:QuerySet = Post.objects.filter(id=pk)
    serializer:PostSerializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)


def put_single_blogpost(request:Request, pk:int) -> Response:
    """Updates Post object given the Post's id.

    Args:
        request (rest_framework.request.Request): HTTP request methods (PUT)
        pk (int): The id of the Blog Post to update in Django
    
    Return:
        Response: JSON data confirming that HTTP PUT was successful for the Blog Post
    """
    try:
        serializer:PostSerializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            blog_post = Post.objects.get(id=pk)
            blog_post.title = serializer.data['title']
            blog_post.post_content = serializer.data['post_content']
            blog_post.save(force_update=True)
            return Response({"success": True, "post_id": blog_post.id})
    except Exception as e:
        print (e)
        return Response({"success": False }, status = status.HTTP_400_BAD_REQUEST)


def delete_single_blogpost(request:Request, pk:int) -> Response:
    """Deletes Post object given the Post's id.

    Args:
        request (rest_framework.request.Request): HTTP request methods (DELETE)
        pk (int): The id of the Blog Post to delete in Django
    
    Return:
        Response: JSON data confirming that HTTP Delete was successful for the Blog Post
    """
    try:
        blog_post = Post.objects.get(id=pk)
        blog_post.delete()
        return Response({"success": True, "post_id": blog_post.id})
    except Exception as e:
        print (e)
        return Response({"success": False }, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def post_utils(request:Request, pk: int) -> None:
    """Handles various HTTP methods (GET, PUT, or DELETE) that happen on /api/posts/<int:pk>/.

    Args:
        request (rest_framework.request.Request): HTTP request methods (GET, PUT, or DELETE)
        pk (int): The id of the Blog Post to perform the HTTP method on in Django
    
    """
    match request.method:
        case 'GET':
            return get_single_blogpost(request, pk)
        case 'PUT':
            return put_single_blogpost(request, pk)
        case 'DELETE':
            return delete_single_blogpost(request, pk)
        case _ :
            print('mmmmmm whoops something didnt go right')
###############################################################################################################



# COMMENT ########################################################################################################
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_comments(request:Request) -> Response:
    """Queries all Comment objects in Django's db and returns a JSON response containing them all.

    Args:
        request (rest_framework.request.Request): HTTP request method (GET)
    
    Return:
        Response: JSON data for all Comments in Django's db
    """
    queryset:QuerySet = Comment.objects.all()
    serializer:CommentSerializer = CommentSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_new_comment_on(request:Request, pk:int) -> Response:
    """Creates new Comment on Post with given id

    Args:
        request (rest_framework.request.Request): HTTP request methods (POST)
        pk (int): The id of the Blog Post to comment on
    
    Return:
        Response: JSON data confirming that HTTP POST was successful for the Blog Post
    """
    print(pk)
    print (request.data)
    serializer:CommentSerializer = CommentSerializer(data=request.data)
    print (serializer)
    if serializer.is_valid():
        comment = Comment.objects.create(
            post = Post.objects.get(id=pk),
            commenter = User.objects.get(id=serializer.data['commenter']),
            comment_content = serializer.data['comment_content']
        )
        comment.save()
        return Response({"success": True, "comment_id": comment.id})
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


def get_single_comment(request:Request, pk:int):
    """Queries Comment objects in Django's db where the Comment's id = the passed pk, Returns a JSON response containing
    data of that comment.

    Args:
        request (rest_framework.request.Request): HTTP request methods (GET)
        pk (int): The id of the Comment in Django
    
    Return:
        Response: JSON data for Comment in Django's db, specified by pk/id
    """
    queryset:QuerySet = Comment.objects.filter(id=pk)
    serializer:CommentSerializer = CommentSerializer(queryset, many=True)
    return Response(serializer.data)


def put_single_comment(request:Request, pk:int) -> Response:
    """Updates Comment object given the Comment's id.

    Args:
        request (rest_framework.request.Request): HTTP request methods (PUT)
        pk (int): The id of the Comment to update in Django
    
    Return:
        Response: JSON data confirming that HTTP PUT was successful for the Comment
    """
    try:
        serializer:CommentSerializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = Comment.objects.get(id=pk)
            comment.comment_content = serializer.data['comment_content']
            comment.save(force_update=True)
            return Response({"success": True, "comment_id": comment.id})
    except Exception as e:
        print (e)
        return Response({"success": False }, status = status.HTTP_400_BAD_REQUEST)


def delete_single_comment(request:Request, pk:int) -> Response:
    """Deletes Comment object given the Comment's id.

    Args:
        request (rest_framework.request.Request): HTTP request methods (DELETE)
        pk (int): The id of the Comment to delete in Django
    
    Return:
        Response: JSON data confirming that HTTP Delete was successful for the Comment
    """
    try:
        comment = Comment.objects.get(id=pk)
        deleted_id:int = comment.id
        comment.delete()
        return Response({"success": True, "comment_id": deleted_id})
    except Exception as e:
        print (e)
        return Response({"success": False }, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def comment_utils(request:Request, pk: int) -> None:
    """Handles various HTTP methods (GET, PUT, or DELETE) that happen on /api/posts/<int:pk>/.

    Args:
        request (rest_framework.request.Request): HTTP request methods (GET, PUT, or DELETE)
        pk (int): The id of the Comment to perform the HTTP method on in Django
    
    """
    match request.method:
        case 'GET':
            return get_single_comment(request, pk)
        case 'PUT':
            return put_single_comment(request, pk)
        case 'DELETE':
            return delete_single_comment(request, pk)
        case _ :
            print('mmmmmm whoops something didnt go right')
###############################################################################################################
