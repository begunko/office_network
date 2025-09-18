# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    skills = models.TextField('Сильные навыки', blank=True)
    position = models.CharField('Должность', max_length=100, blank=True)
    is_approved = models.BooleanField('Подтверждённый аккаунт', default=False)
    
    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"