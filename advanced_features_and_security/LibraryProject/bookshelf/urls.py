from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('', views.book_list, name='book_list'),
    path('about/', views.about, name='about'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:book_id>/', views.book_detail, name='book-detail'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('class-books/', views.BookListView.as_view(), name='book_list_class'),
]