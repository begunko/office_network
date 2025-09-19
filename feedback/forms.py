# feedback/forms.py
from django import forms
from .models import Feedback, FeedbackAttachment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FeedbackForm(forms.ModelForm):
    attachments = MultipleFileField(
        required=False,
        label='Прикрепленные файлы'
    )

    class Meta:
        model = Feedback
        fields = ['title', 'content', 'feedback_type', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Краткое описание'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Подробное описание вашего предложения или проблемы'}),
            'feedback_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'feedback_type': 'Тип обратной связи',
            'priority': 'Приоритет',
        }

    def save(self, commit=True):
        feedback = super().save(commit=False)
        if commit:
            feedback.save()

            # Сохраняем прикрепленные файлы
            for file in self.files.getlist('attachments'):
                FeedbackAttachment.objects.create(feedback=feedback, file=file)

        return feedback


class FeedbackResponseForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['is_processed', 'response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ответ на обратную связь'}),
        }
        labels = {
            'is_processed': 'Отметить как обработанное',
            'response': 'Ответ',
        }
