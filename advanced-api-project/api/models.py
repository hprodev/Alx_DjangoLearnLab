from django.db import models

class Author(models.Model):
    """
    Author model represents a book author.
    
    Fields:
        name: CharField storing the author's full name
    
    Relationships:
        Has a one-to-many relationship with Book model
        (one author can write multiple books)
    """
    name = models.CharField(max_length=200, help_text="Author's full name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model represents a book in the library.
    
    Fields:
        title: CharField storing the book's title
        publication_year: IntegerField for the year of publication
        author: ForeignKey linking to the Author model
    
    Relationships:
        Many-to-one relationship with Author
        (multiple books can have the same author)
    """
    title = models.CharField(max_length=200, help_text="Book title")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author who wrote this book"
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        ordering = ['-publication_year', 'title']