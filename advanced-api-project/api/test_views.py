from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book
from datetime import datetime

class BookAPITestCase(TestCase):
    """
    Comprehensive unit tests for Book API endpoints.
    
    Tests cover:
    - CRUD operations (Create, Read, Update, Delete)
    - Authentication and permissions
    - Filtering, searching, and ordering
    - Data validation and error handling
    """
    
    def setUp(self):
        """
        Set up test data and client before each test.
        Creates test user, author, and books for testing.
        """
        # Create API client
        self.client = APIClient()
        
        # Create test user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(name="Test Author")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Test Book 1",
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Test Book 2",
            publication_year=2021,
            author=self.author
        )
    
    def test_list_books_unauthenticated(self):
        """
        Test that unauthenticated users can view the list of books.
        Verifies read-only access for non-authenticated users.
        """
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_retrieve_book_detail(self):
        """
        Test retrieving a single book by ID.
        Verifies the detail view returns correct book data.
        """
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book 1')
        self.assertEqual(response.data['publication_year'], 2020)
    
    def test_create_book_authenticated(self):
        """
        Test creating a book with authentication.
        Verifies authenticated users can create new books.
        """
        # Authenticate
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'New Test Book',
            'publication_year': 2022,
            'author': self.author.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.latest('id').title, 'New Test Book')
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        Verifies permission controls are working.
        """
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2022,
            'author': self.author.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # No new book created
    
    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication.
        Verifies authenticated users can update existing books.
        """
        # Authenticate
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Updated Book Title',
            'publication_year': 2020,
            'author': self.author.id
        }
        
        response = self.client.put(f'/api/books/{self.book1.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify update
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_update_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        Verifies permission controls for update operations.
        """
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 2020,
            'author': self.author.id
        }
        
        response = self.client.put(f'/api/books/{self.book1.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify no update occurred
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Test Book 1')
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication.
        Verifies authenticated users can delete books.
        """
        # Authenticate
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)  # One book remaining
    
    def test_delete_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        Verifies permission controls for delete operations.
        """
        response = self.client.delete(f'/api/books/{self.book1.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # No books deleted
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author.
        Verifies the filtering functionality works correctly.
        """
        # Create another author and book
        author2 = Author.objects.create(name="Another Author")
        Book.objects.create(
            title="Different Book",
            publication_year=2019,
            author=author2
        )
        
        response = self.client.get(f'/api/books/?author={self.author.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only books by first author
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        response = self.client.get('/api/books/?publication_year=2020')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
    
    def test_search_books(self):
        """
        Test searching books by title and author name.
        Verifies search functionality works correctly.
        """
        response = self.client.get('/api/books/?search=Test Book 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
    
    def test_order_books_by_title(self):
        """
        Test ordering books by title.
        Verifies ordering functionality works correctly.
        """
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        self.assertEqual(response.data[1]['title'], 'Test Book 2')
    
    def test_order_books_by_publication_year_desc(self):
        """
        Test ordering books by publication year in descending order.
        """
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)
        self.assertEqual(response.data[1]['publication_year'], 2020)
    
    def test_validate_future_publication_year(self):
        """
        Test that validation prevents future publication years.
        Verifies custom validation in BookSerializer works.
        """
        # Authenticate
        self.client.login(username='testuser', password='testpass123')
        
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.id
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_missing_fields(self):
        """
        Test that creating a book with missing fields returns validation error.
        """
        # Authenticate
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'title': 'Incomplete Book',
            # Missing publication_year and author
        }
        
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)