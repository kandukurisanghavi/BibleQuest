from django.db import models
from django.contrib.auth.models import User

class QuizQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)  # Store 'a', 'b', 'c', or 'd'
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return self.question

class VerseOfTheDay(models.Model):
    reference = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return f"{self.reference} - {self.text}"

from django.db import models
from django.contrib.auth.models import User

class PrayerRequest(models.Model):
    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('family', 'Family'),
        ('career', 'Career'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')  # New field
    timestamp = models.DateTimeField(auto_now_add=True)
    prayed_count = models.PositiveIntegerField(default=0)  # Optional: Track how many times it has been prayed for

    def __str__(self):
        return f"{self.user.username} - {self.text[:50]}"
    
class Comment(models.Model):
    prayer_request = models.ForeignKey(PrayerRequest, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:50]}"