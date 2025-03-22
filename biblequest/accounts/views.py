from django.shortcuts import render, redirect, get_object_or_404  # Added get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import QuizQuestion, VerseOfTheDay, PrayerRequest, Comment  # Import Comment model
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
    user_name = request.user.username

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
    verse = verses[day_of_year % len(verses)]
    return render(request, 'accounts/verse_of_the_day.html', {'verse': verse, 'date': today})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def prayer_request(request):
    form_submitted = False  # Track whether the form has been submitted
    success_message = None  # Initialize the success message variable

    if request.method == 'POST':
        prayer_text = request.POST.get('prayer_request')
        if prayer_text:
            PrayerRequest.objects.create(user=request.user, text=prayer_text)
            success_message = "Your prayer request has been submitted."  # Set the success message
            form_submitted = True  # Mark the form as submitted

    return render(request, 'accounts/prayer_request.html', {
        'form_submitted': form_submitted,  # Pass the form submission status to the template
        'success_message': success_message  # Pass the success message to the template
    })


# View Prayer Requests (Prayer Wall)
@login_required
def view_prayer_requests(request):
    prayer_requests = PrayerRequest.objects.all().order_by('-timestamp')
    return render(request, 'accounts/view_prayer_requests.html', {'prayer_requests': prayer_requests})


# Add Comment to a Prayer Request
@login_required
def add_comment(request, prayer_request_id):
    if request.method == 'POST':
        prayer_request = get_object_or_404(PrayerRequest, id=prayer_request_id)
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(prayer_request=prayer_request, user=request.user, text=comment_text)
            messages.success(request, "Your comment has been added.")
        return redirect('view_prayer_requests')