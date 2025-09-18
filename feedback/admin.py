# feedback/admin.py
from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('content',)
    date_hierarchy = 'created_at'
