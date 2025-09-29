from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    API view to retrieve list of all books.
    
    - GET: Returns a list of all books
    - Permissions: Read-only access for unauthenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read, only authenticated can modify


class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by ID.
    
    - GET: Returns details of a specific book
    - Permissions: Read-only access for unauthenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    - POST: Create a new book instance
    - Permissions: Only authenticated users can create books
    - Handles form submission and data validation through BookSerializer
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create


class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    - PUT/PATCH: Update a book instance
    - Permissions: Only authenticated users can update books
    - Handles form submission and data validation through BookSerializer
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update


class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    - DELETE: Remove a book instance from the database
    - Permissions: Only authenticated users can delete books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete