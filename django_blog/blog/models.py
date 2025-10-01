from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Post(models.Model):
    """
    Blog post model representing individual blog entries.
    
    Fields:
        title: The title of the blog post
        content: The main content/body of the post
        published_date: Timestamp when the post was created
        author: Foreign key to User model, the author of the post
        tags: Many-to-many relationship with Tag model via taggit
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()  # Add this line
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date']


class Comment(models.Model):
    """
    Comment model for user comments on blog posts.
    
    Fields:
        post: Foreign key to Post model (many-to-one relationship)
        author: Foreign key to User model, the comment author
        content: The text content of the comment
        created_at: Timestamp when comment was created
        updated_at: Timestamp when comment was last updated
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    class Meta:
        ordering = ['created_at']