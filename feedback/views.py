# feedback/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Feedback, FeedbackAttachment
from .forms import FeedbackForm, FeedbackResponseForm


@login_required
def feedback_list(request):
    if request.user.is_staff:
        feedbacks = Feedback.objects.all().order_by('-created_at')
    else:
        feedbacks = Feedback.objects.filter(
            author=request.user).order_by('-created_at')

    # Фильтрация по типу
    feedback_type = request.GET.get('type')
    if feedback_type:
        feedbacks = feedbacks.filter(feedback_type=feedback_type)

    # Фильтрация по статусу
    status = request.GET.get('status')
    if status == 'processed':
        feedbacks = feedbacks.filter(is_processed=True)
    elif status == 'unprocessed':
        feedbacks = feedbacks.filter(is_processed=False)

    # Получаем типы обратной связи для фильтров
    feedback_types = Feedback.FEEDBACK_TYPES

    return render(request, 'feedback/feedback_list.html', {
        'feedbacks': feedbacks,
        'current_type': feedback_type,
        'current_status': status,
        'feedback_types': feedback_types
    })


@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.author = request.user
            feedback.save()
            messages.success(
                request, 'Ваша обратная связь успешно отправлена!')
            return redirect('feedback_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_create.html', {'form': form})


@login_required
def feedback_detail(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    # Проверяем, может ли пользователь просматривать эту обратную связь
    if not request.user.is_staff and feedback.author != request.user:
        messages.error(
            request, 'У вас нет прав для просмотра этой обратной связи')
        return redirect('feedback_list')

    # Получаем вложения для этой обратной связи
    attachments = feedback.attachments.all()

    response_form = None
    if request.user.is_staff:
        response_form = FeedbackResponseForm(instance=feedback)

    return render(request, 'feedback/feedback_detail.html', {
        'feedback': feedback,
        'attachments': attachments,
        'response_form': response_form
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def feedback_process(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == 'POST':
        form = FeedbackResponseForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            if feedback.is_processed and not feedback.processed_by:
                feedback.processed_by = request.user
                feedback.processed_at = timezone.now()
            feedback.save()
            messages.success(request, 'Обратная связь успешно обновлена!')
            return redirect('feedback_detail', feedback_id=feedback.id)

    return redirect('feedback_detail', feedback_id=feedback.id)
