from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    genre = models.CharField(max_length=50)
    published_date = models.DateField()
    pages = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    # created_at line removed

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']  # Changed from ['-created_at'] to ['title']