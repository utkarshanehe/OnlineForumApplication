from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from .forms import CreatePostForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    forums = Category.objects.all()
    number_of_posts = Post.objects.all().count()
    number_of_users = User.objects.all().count()
    number_of_forums = forums.count()

    try:
        last_post = Post.objects.latest("timestamp")
    except:
        last_post = []

    context = {
        'forums': forums,
        'number_of_posts': number_of_posts,
        'number_of_users': number_of_users,
        'number_of_forums': number_of_forums,
        'last_post': last_post,
        'title': 'Forum App'
    }
    return render(request, 'index.html', context)


def show_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)

    # Pagination for the posts
    paginator = Paginator(posts, 10)
    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'forum': category,
        'title': category.title + ' Posts',
    }
    return render(request, 'posts.html', context)


def show_post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)

    # Save comment for the post in the database
    if "comment-form" in request.POST:
        comment = request.POST.get("comment-input")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    # Save reply for the comment in the database
    if "reply-form" in request.POST:
        reply = request.POST.get("reply-input")
        comment_id = request.POST.get("comment-id")
        comment_object = Comment.objects.get(id=comment_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_object.replies.add(new_reply.id)

    context = {
        'post': post,
        'title': post.title,
    }
    update_views(request, post)
    return render(request, 'post_detail.html', context)


@login_required
def create_post(request):
    context = {}
    form = CreatePostForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                author = Author.objects.get(user=request.user)
            except Author.DoesNotExist:
                author = None

            form.instance.author = author
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()

            return redirect("index")

    context.update({
        "form": form,
        "title": "Create New Post"
    })
    return render(request, "create_post.html", context)
