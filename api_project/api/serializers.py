# api/serializers.py

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model
        
    def validate_isbn(self, value):
        """
        Check that the ISBN is 13 digits long
        """
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be exactly 13 characters long.")
        return value