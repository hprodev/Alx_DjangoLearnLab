from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.urls import reverse_lazy
from .models import Book, Author
from .models import Library

# Task 1: Function-based view to list all books
def list_books(request):
    """Function-based view that lists all books."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Task 1: Class-based view for library details
class LibraryDetailView(DetailView):
    """Class-based view that displays details for a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Task 2: User Registration View
def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Task 2: Custom Login View
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True


# Task 2: Custom Logout View
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'


# Task 3: Helper function to check user roles
def check_role(user, role):
    """Helper function to check if user has specific role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == role


# Task 3: Role-based view functions
@login_required
@user_passes_test(lambda user: check_role(user, 'Admin'))
def admin_view(request):
    """Admin view accessible only to Admin users."""
    return render(request, 'relationship_app/admin_view.html')


@login_required
@user_passes_test(lambda user: check_role(user, 'Librarian'))
def librarian_view(request):
    """Librarian view accessible only to Librarian users."""
    return render(request, 'relationship_app/librarian_view.html')


@login_required
@user_passes_test(lambda user: check_role(user, 'Member'))
def member_view(request):
    """Member view accessible only to Member users."""
    return render(request, 'relationship_app/member_view.html')


# Task 4: Permission-based views for Book operations
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a book - requires can_add_book permission."""
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """View to edit a book - requires can_change_book permission."""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            author = get_object_or_404(Author, id=author_id)
            book.title = title
            book.author = author
            book.save()
            return redirect('list_books')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {
        'book': book, 
        'authors': authors
    })


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """View to delete a book - requires can_delete_book permission."""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})