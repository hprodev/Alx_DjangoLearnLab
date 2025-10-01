from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    Blog post model representing individual blog entries.
    
    Fields:
        title: The title of the blog post
        content: The main content/body of the post
        published_date: Timestamp when the post was created
        author: Foreign key to User model, the author of the post
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_date']