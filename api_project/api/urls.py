# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

# Create a router and register our viewset with it
router = DefaultRouter()
router.register(r'books_all', views.BookViewSet, basename='book_all')

urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', views.BookList.as_view(), name='book-list'),
    
    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),
    
    # Authentication endpoint
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
]