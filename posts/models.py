# posts/models.py
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание категории', blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    POST_TYPES = [
        ('problem', 'Проблема'),
        ('suggestion', 'Предложение'),
        ('blog', 'Блог'),
    ]
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание')
    post_type = models.CharField(
        'Тип поста', max_length=20, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return f"{self.title} ({self.get_post_type_display()})"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField('Содержание комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} к посту "{self.post.title}"'


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'

    def __str__(self):
        return f'{self.user.username} лайкнул(а) {self.post.title}'
