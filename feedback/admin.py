# feedback/admin.py
from django.contrib import admin
from django.utils import timezone
from .models import Feedback, FeedbackAttachment


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'feedback_type',
                    'priority', 'is_processed', 'created_at')
    list_filter = ('feedback_type', 'priority', 'is_processed', 'created_at')
    list_editable = ('is_processed', 'priority')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('author', 'title', 'content', 'feedback_type', 'priority')
        }),
        ('Статус обработки', {
            'fields': ('is_processed', 'processed_by', 'processed_at', 'response')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.is_processed and not obj.processed_by:
            obj.processed_by = request.user
            obj.processed_at = timezone.now()
        elif not obj.is_processed:
            obj.processed_by = None
            obj.processed_at = None
        super().save_model(request, obj, form, change)


@admin.register(FeedbackAttachment)
class FeedbackAttachmentAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('feedback__title',)
