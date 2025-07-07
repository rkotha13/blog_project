from django.shortcuts import render, redirect
from .models import BlogPost, Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.shortcuts import get_object_or_404

from .forms import BlogPostForm

@login_required
def home(request):
    posts = BlogPost.objects.select_related('author').prefetch_related('categories').order_by('-created_at')
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'posts': posts})

@login_required
def post_list(request):
    posts = BlogPost.objects.select_related('author').prefetch_related('categories').order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # For categories
            return redirect('post_list')
    else:
        form = BlogPostForm()
    return render(request, 'post_create.html', {'form': form})

def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'post_detail.html', {'post': post})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return render(request, 'logged_out.html')