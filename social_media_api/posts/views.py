from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, permissions, status

def create_notification(recipient, actor, verb, target=None):
    """
    Helper function to create notifications.
    """
    from notifications.models import Notification
    
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb
    )
    
    if target:
        notification.target = target
        notification.save()
    
    return notification

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only author can edit/delete their own posts/comments.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.author == request.user


class StandardResultsPagination(PageNumberPagination):
    """
    Pagination settings: 10 items per page.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on posts.
    - List all posts
    - Create new post
    - Retrieve single post
    - Update post (author only)
    - Delete post (author only)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    
    def perform_create(self, serializer):
        """Set the post author to the current user"""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on comments.
    - List all comments
    - Create new comment
    - Retrieve single comment
    - Update comment (author only)
    - Delete comment (author only)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsPagination
    
    def perform_create(self, serializer):
        """Set the comment author to the current user"""
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    """
    Get personalized feed showing posts from users you follow.
    """
    # Get all users that current user follows
    following_users = request.user.following.all()
    
    # Get posts from those users, newest first
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Apply pagination
    paginator = StandardResultsPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    
    # Convert to JSON
    serializer = PostSerializer(paginated_posts, many=True)
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """
    Like a post and notify the author.
    """
    try:
        post = generics.get_object_or_404(Post, pk=pk)
    except:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Try to create like (will fail if already exists)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        return Response(
            {'message': 'You already liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create notification if not liking own post
    if post.author != request.user:
        create_notification(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )
    
    return Response(
        {'message': 'Post liked successfully'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """
    Unlike a post.
    """
    try:
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        
        return Response(
            {'message': 'Post unliked successfully'},
            status=status.HTTP_200_OK
        )
    
    except Post.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Like.DoesNotExist:
        return Response(
            {'error': 'You have not liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )