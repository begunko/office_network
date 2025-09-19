# feedback/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('suggestion', 'Предложение'),
        ('problem', 'Проблема'),
        ('improvement', 'Идея улучшения'),
        ('other', 'Другое'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200,
                             default='Без заголовка')  # Добавим default
    content = models.TextField('Содержание обратной связи')
    feedback_type = models.CharField(
        'Тип обратной связи', max_length=20, choices=FEEDBACK_TYPES, default='suggestion')
    priority = models.CharField(
        'Приоритет', max_length=10, choices=PRIORITY_LEVELS, default='medium')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_processed = models.BooleanField('Обработано', default=False)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='processed_feedbacks', verbose_name='Кем обработано')
    processed_at = models.DateTimeField(
        'Когда обработано', null=True, blank=True)
    response = models.TextField('Ответ на обратную связь', blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'обратная связь'
        verbose_name_plural = 'обратные связи'

    def __str__(self):
        return f"{self.title} ({self.get_feedback_type_display()})"


class FeedbackAttachment(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='feedback_attachments/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.feedback.title}"
