# feedback/models.py
from django.db import models
from users.models import User

class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('Содержание обратной связи')
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'пост'  # или 'обратная связь'
        verbose_name_plural = 'посты'  # или 'обратные связи'