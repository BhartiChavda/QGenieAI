from django.contrib import admin
from .models import UploadedFile, Question, QuizResult

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UploadedFile model.
    Enables listing, searching, and filtering of user uploads.
    """
    list_display = ('title', 'user', 'file_type', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('title', 'user__username', 'user__email')
    ordering = ('-uploaded_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Question model.
    Enables tracking of generated questions and their correct keys.
    """
    list_display = ('get_question_snippet', 'file', 'correct_answer')
    list_filter = ('file__file_type', 'correct_answer')
    search_fields = ('question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'explanation')
    
    def get_question_snippet(self, obj):
        return obj.question_text[:60] + "..." if len(obj.question_text) > 60 else obj.question_text
    get_question_snippet.short_description = 'Question Text'


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizResult model.
    Displays user performance scores, percentages, and attempt timestamps.
    """
    list_display = ('user', 'file', 'score', 'total_questions', 'percentage', 'date_taken')
    list_filter = ('date_taken', 'percentage')
    search_fields = ('user__username', 'file__title')
    ordering = ('-date_taken',)
