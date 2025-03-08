# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import QuizQuestion, VerseOfTheDay
import random
import datetime

# Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

# Home View
@login_required
def home(request):
    current_hour = datetime.datetime.now().hour
    user_name = request.user.username  # Assuming the user is logged in and authenticated

    if current_hour < 12:
        greeting = 'Good morning'
    elif 12 <= current_hour < 18:
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'

    context = {
        'greeting': f"{greeting}, {user_name}! Welcome!"
    }
    return render(request, 'accounts/home.html', context)

# Quiz View
@login_required
def select_difficulty(request):
    return render(request, 'accounts/select_difficulty.html')

def quiz(request, difficulty):
    questions = QuizQuestion.objects.filter(difficulty=difficulty).order_by('?')[:10]
    return render(request, 'accounts/quiz.html', {'questions': questions})

# Verse of the Day View
@login_required
def verse_of_the_day(request):
    verses = list(VerseOfTheDay.objects.all())
    today = datetime.date.today()
    day_of_year = today.timetuple().tm_yday
    verse = verses[day_of_year % len(verses)]  # Select a verse based on the day of the year
    return render(request, 'accounts/verse_of_the_day.html', {'verse': verse, 'date': today})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

def prayer_request(request):
    return render(request, 'accounts/prayer_request.html')