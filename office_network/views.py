# core/views.py
from django.shortcuts import render
from posts.models import Post

def home(request):
    posts = Post.objects.all()[:10]
    return render(request, 'core/home.html', {'posts': posts})