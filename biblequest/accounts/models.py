# accounts/models.py
from django.db import models

class QuizQuestion(models.Model):
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)  # Store 'a', 'b', 'c', or 'd'

    def __str__(self):
        return self.question

class VerseOfTheDay(models.Model):
    reference = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"{self.reference} - {self.text}"