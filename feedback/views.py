# feedback/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback

@login_required
def feedback_list(request):
    if request.user.is_staff:
        feedbacks = Feedback.objects.all().order_by('-created_at')
    else:
        feedbacks = Feedback.objects.filter(author=request.user).order_by('-created_at')
    
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def feedback_create(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Feedback.objects.create(
                author=request.user,
                content=content
            )
            messages.success(request, 'Обратная связь отправлена!')
            return redirect('feedback_list')
    
    return render(request, 'feedback/feedback_create.html')