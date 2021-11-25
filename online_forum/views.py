from django.shortcuts import render, get_object_or_404
from .models import Author, Category, Post
from .utils import update_views


def index(request):
    forums = Category.objects.all()
    context = {'forums': forums}
    return render(request, 'index.html', context)


def show_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    context = {'posts': posts}
    print(posts)
    return render(request, 'posts.html', context)


def show_post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post}
    update_views(request, post)
    print(post.title)
    print(post.comments)
    return render(request, 'post_detail.html', context)
