from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm

def home(request):
    """Home page view"""
    return render(request, 'blog/home.html')


def register(request):
    """
    User registration view.
    Handles GET request to display registration form and
    POST request to create new user account.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """
    User profile view.
    Displays and allows editing of user profile information.
    Requires user to be logged in.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {'form': form})

class PostListView(ListView):
    """
    Display list of all blog posts.
    Uses ListView generic view to show all posts ordered by published date.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):
    """
    Display individual blog post details.
    Shows full content of a single post.
    """
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        """Add comment form and comments to context"""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create new blog post.
    Requires user to be logged in.
    Automatically sets the author to the current user.
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags']
    fields = ['title', 'content']
    success_url = reverse_lazy('posts')
    
    def form_valid(self, form):
        """Set the post author to the current user before saving"""
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update existing blog post.
    Requires user to be logged in and be the author of the post.
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags']
    fields = ['title', 'content']
    success_url = reverse_lazy('posts')
    
    def form_valid(self, form):
        """Maintain the original author when updating"""
        form.instance.author = self.request.user
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Check if the current user is the author of the post"""
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete blog post.
    Requires user to be logged in and be the author of the post.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts')
    
    def test_func(self):
        """Check if the current user is the author of the post"""
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        """Add success message when post is deleted"""
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
@login_required
def add_comment(request, pk):
    """
    Add a comment to a blog post.
    Requires user to be logged in.
    
    Args:
        pk: Primary key of the post to comment on
    """
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment.html', {
        'form': form,
        'post': post
    })


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing comment.
    Only the comment author can edit their comment.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def test_func(self):
        """Check if current user is the comment author"""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """Redirect to the post detail page after successful update"""
        messages.success(self.request, 'Comment updated successfully!')
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a comment.
    Only the comment author can delete their comment.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        """Check if current user is the comment author"""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        """Redirect to the post detail page after deletion"""
        messages.success(self.request, 'Comment deleted successfully!')
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
def search_posts(request):
    """
    Search posts by title, content, or tags.
    Uses Q objects for complex queries.
    """
    query = request.GET.get('q', '')
    posts = Post.objects.none()
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'query': query
    })


def posts_by_tag(request, tag_name):
    """
    Display all posts with a specific tag.
    
    Args:
        tag_name: The name of the tag to filter by
    """
    posts = Post.objects.filter(tags__name=tag_name)
    
    return render(request, 'blog/posts_by_tag.html', {
        'posts': posts,
        'tag_name': tag_name
    })