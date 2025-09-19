# api/views.py

from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all books.
    Only authenticated users can access this view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    Provides CRUD operations: Create, Read, Update, Delete
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def set_favorite(self, request, pk=None):
        """
        Custom action to mark a book as favorite
        """
        book = self.get_object()
        # You can add custom logic here
        return Response({'status': f'{book.title} marked as favorite'})
    
    @action(detail=False)
    def recent_books(self, request):
        """
        Custom action to get recently added books
        """
        recent = Book.objects.all()[:5]  # Get last 5 books
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)