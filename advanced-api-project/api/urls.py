from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # List all books
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Create a new book (must come before detail view to avoid conflict)
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Retrieve a single book by ID
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Update an existing book
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]