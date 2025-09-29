from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization of Book model instances.
    
    Serializes all fields of the Book model and includes custom validation
    to ensure the publication_year is not in the future.
    
    Validation:
        - publication_year: Must not be greater than the current year
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Serializes all fields: id, title, publication_year, author
    
    def validate_publication_year(self, value):
        """
        Custom validation to ensure publication_year is not in the future.
        
        Args:
            value: The publication_year value to validate
            
        Returns:
            The validated publication_year value
            
        Raises:
            serializers.ValidationError: If publication_year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization of Author model instances.
    
    This serializer includes nested serialization of related Book instances,
    dynamically serializing all books written by the author using the
    'books' related_name from the Book model's ForeignKey.
    
    Fields:
        - name: The author's name
        - books: Nested serialization of all books by this author
    
    The nested BookSerializer is read-only and serializes the complete
    book information including title, publication_year, and author reference.
    """
    # Nested serializer for the related books
    # 'books' matches the related_name in the Book model's ForeignKey
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Explicitly define fields including nested books