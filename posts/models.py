# posts/models.py
from django.db import models
from users.models import User


class Post(models.Model):
    POST_TYPES = [
        ('problem', 'Проблема'),
        ('suggestion', 'Предложение'),
        ('blog', 'Блог'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    post_type = models.CharField(
        'Тип поста', max_length=20, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'пост'  # или 'обратная связь'
        verbose_name_plural = 'посты'  # или 'обратные связи'

    def __str__(self):
        return f"{self.title} ({self.get_post_type_display()})"
