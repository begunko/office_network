# feedback/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('create/', views.feedback_create, name='feedback_create'),
    path('<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
    path('<int:feedback_id>/process/',
         views.feedback_process, name='feedback_process'),
]

# Добавляем маршрут для обслуживания медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
