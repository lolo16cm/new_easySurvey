from django.db import models
from userauths.models import User
# Create your models here.

  
class Survey(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='survey_creator', verbose_name="Created by")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} is created at {self.created_at}'


# the questions in the survey
class Question(models.Model):
    # list of tuples k, value
    QUESTION_TYPES = [
        ('short_text', 'Short Text'),
        ('multiple_choice', 'Multiple Choice'),
        ('checkbox', 'Checkbox'),
        ('dropdown', 'Dropdown'),
    ]

    form = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    required = models.BooleanField(default=False)  # Indicates if this question is required

    def __str__(self):
        return self.text


class Option(models.Model):
    """Represents an option for questions that have multiple choices (e.g., Multiple Choice, Checkbox, Dropdown)."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text