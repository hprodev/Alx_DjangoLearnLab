from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework

class BookListView(generics.ListAPIView):
    """
    API view to retrieve list of all books with filtering, searching, and ordering.
    
    - GET: Returns a list of all books
    - Permissions: Read-only access for unauthenticated users
    
    Filtering:
        - Filter by title: ?title=Harry Potter
        - Filter by author: ?author=1
        - Filter by publication_year: ?publication_year=1997
    
    Searching:
        - Search in title and author name: ?search=Harry
    
    Ordering:
        - Order by any field: ?ordering=title
        - Reverse order: ?ordering=-publication_year
        - Multiple fields: ?ordering=author,title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['title', 'author', 'publication_year']
    
    search_fields = ['title', 'author__name']
    
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering

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