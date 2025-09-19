# core/views.py
from django.shortcuts import render
from posts.models import Post

def home(request):
    posts = Post.objects.all()[:5]  # Последние 5 постов
    return render(request, 'core/home.html', {'posts': posts})