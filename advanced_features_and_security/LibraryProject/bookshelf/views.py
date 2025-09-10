from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book

def home(request):
    featured_books = Book.objects.all()[:6]
    context = {
        'featured_books': featured_books,
    }
    return render(request, 'home.html', context)

def book_list(request):
    books = Book.objects.all()
    
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(title__icontains=search_query)
    
    genre_filter = request.GET.get('genre')
    if genre_filter:
        books = books.filter(genre=genre_filter)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    book_list = paginator.get_page(page_number)
    
    context = {
        'book_list': book_list,
    }
    return render(request, 'book_list.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {
        'book': book,
    }
    return render(request, 'book_detail.html', context)

def about(request):
    context = {
        'total_books': Book.objects.count(),
        'happy_customers': '5000+',
        'years_serving': '4',
    }
    return render(request, 'about.html', context)