from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments.
    Shows comment details with author information.
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 
                  'created_at', 'updated_at']
        read_only_fields = ['author']


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for posts.
    Shows post details with author info and comment count.
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 
                  'created_at', 'updated_at', 'comments_count']
        read_only_fields = ['author']
    
    def get_comments_count(self, obj):
        """Count number of comments on this post"""
        return obj.comments.count()