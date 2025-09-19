# posts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Post, Comment, Like, Category
from .forms import CommentForm


def post_list(request):
    post_type = request.GET.get('type')
    if post_type:
        posts = Post.objects.filter(
            post_type=post_type).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = post.likes.filter(user=request.user).exists()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'user_has_liked': user_has_liked
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post_type = request.POST.get('post_type')
        category_id = request.POST.get('category')

        if title and content and post_type:
            post = Post.objects.create(
                title=title,
                content=content,
                post_type=post_type,
                author=request.user
            )

            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                    post.category = category
                    post.save()
                except Category.DoesNotExist:
                    pass

            messages.success(request, 'Пост успешно создан!')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'Заполните все обязательные поля')

    categories = Category.objects.all()
    return render(request, 'posts/post_create.html', {'categories': categories})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    return redirect('post_detail', post_id=post.id)


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post_detail', post_id=post.id)


def post_search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        posts = Post.objects.none()
    return render(request, 'posts/search_results.html', {'posts': posts, 'query': query})
