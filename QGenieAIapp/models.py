from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


class UploadedFile(models.Model):
    """
    Model representing files uploaded by users for generating MCQs.
    Supports PDF and TXT file formats.
    """
    FILE_TYPES = [
        ('PDF', 'PDF Document'),
        ('TXT', 'Plain Text File'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='uploads/')
    title = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    include_answers = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Advanced AI Metadata Fields
    summary_markdown = models.TextField(blank=True, null=True)
    detected_topic = models.CharField(max_length=100, blank=True, null=True)
    difficulty = models.CharField(max_length=20, default='medium')

    def __str__(self):
        return f"{self.title} ({self.file_type}) - Uploaded by {self.user.username}"

    def filename(self):
        return os.path.basename(self.file.name)


class Question(models.Model):
    """
    Model representing Multiple Choice Questions generated from an UploadedFile.
    Stores the question text, 4 options, the correct answer, and an optional explanation.
    """
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Question for {self.file.title}: {self.question_text[:50]}..."


class NormalQuestion(models.Model):
    """
    Model representing normal subjective questions generated from an UploadedFile.
    Stores the question text and an AI generated answer/explanation.
    """
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='normal_questions')
    question_text = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"Normal Question for {self.file.title}: {self.question_text[:50]}..."


class QuizResult(models.Model):
    """
    Model representing user's quiz attempt history.
    Stores the user, the source file, questions answered, score, percentage, and date.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    file = models.ForeignKey(UploadedFile, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    selected_answers_json = models.TextField(blank=True, null=True)  # Stores JSON of user answers for historical view
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}/{self.total_questions} ({self.percentage}%)"


class OTPVerification(models.Model):
    """
    Model representing one-time passwords for email verification.
    Set to delete when the corresponding User account is deleted.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp_verification')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.user.username} (Expires at {self.expires_at})"


class UserProfile(models.Model):
    """
    Model representing user settings, profile photo, and visual preferences.
    """
    THEME_CHOICES = [
        ('indigo', 'Indigo Glow'),
        ('emerald', 'Emerald Forest'),
        ('rose', 'Rose Quartz'),
        ('amber', 'Amber Gold'),
        ('dark', 'Midnight Dark'),
    ]
    THEME_MODE_CHOICES = [
        ('light', 'Light Mode'),
        ('dark', 'Dark Mode'),
        ('night', 'Night Mode'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='indigo')
    theme_mode = models.CharField(max_length=20, choices=THEME_MODE_CHOICES, default='dark')

    def __str__(self):
        return f"{self.user.username}'s Profile"


class BookmarkedQuestion(models.Model):
    """
    Model representing user's bookmarked questions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} bookmarked Question #{self.question.id}"


# --- Signals to Auto-Create UserProfile ---
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)



