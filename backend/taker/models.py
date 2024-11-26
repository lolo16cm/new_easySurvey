from django.db import models
from userauths.models import User
from creator.models import Survey, Question, Option

# Response model to store a user's response to a specific survey
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses', verbose_name="Respondent")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response by {self.user} for {self.survey.title}'

# Answer model to store the answer to each question in the survey
class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    # To store the selected option(s) for multiple-choice, checkbox, or dropdown questions
    selected_options = models.ManyToManyField(Option, blank=True)  # only used if question type requires options
    # To store a short text answer if the question type is short_text
    text_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Answer to "{self.question.text}" in response to {self.response}'
