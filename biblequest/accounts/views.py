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
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment, PrayerRequest
from .utils import fetch_bible_data





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
    
    
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        new_text = request.POST.get('comment_text')
        if new_text.strip():  # Ensure the new text is not empty
            comment.text = new_text
            comment.save()
            messages.success(request, "Comment updated successfully.")
        else:
            messages.error(request, "Comment cannot be empty.")
    return redirect('view_prayer_requests')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    return redirect('view_prayer_requests')

from django.shortcuts import render
from .utils import fetch_bible_data

# Define the books of the Bible
OLD_TESTAMENT_BOOKS = {
    "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, "Deuteronomy": 34,
    "Joshua": 24, "Judges": 21, "Ruth": 4, "1 Samuel": 31, "2 Samuel": 24,
    "1 Kings": 22, "2 Kings": 25, "1 Chronicles": 29, "2 Chronicles": 36, "Ezra": 10,
    "Nehemiah": 13, "Esther": 10, "Job": 42, "Psalms": 150, "Proverbs": 31,
    "Ecclesiastes": 12, "Song of Solomon": 8, "Isaiah": 66, "Jeremiah": 52,
    "Lamentations": 5, "Ezekiel": 48, "Daniel": 12, "Hosea": 14, "Joel": 3,
    "Amos": 9, "Obadiah": 1, "Jonah": 4, "Micah": 7, "Nahum": 3, "Habakkuk": 3,
    "Zephaniah": 3, "Haggai": 2, "Zechariah": 14, "Malachi": 4
}

NEW_TESTAMENT_BOOKS = {
    "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28,
    "Romans": 16, "1 Corinthians": 16, "2 Corinthians": 13, "Galatians": 6,
    "Ephesians": 6, "Philippians": 4, "Colossians": 4, "1 Thessalonians": 5,
    "2 Thessalonians": 3, "1 Timothy": 6, "2 Timothy": 4, "Titus": 3,
    "Philemon": 1, "Hebrews": 13, "James": 5, "1 Peter": 5, "2 Peter": 3,
    "1 John": 5, "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22
}

def bible_view(request):
    """
    Handle user requests for Bible data (testament, book, chapter, or verse).
    """
    testament = request.GET.get('testament')  # Old Testament or New Testament
    book = request.GET.get('book')  # Selected book
    chapter = request.GET.get('chapter')  # Selected chapter
    verse = request.GET.get('verse')  # Selected verse
    search_query = request.GET.get('search')  # Search query

    error_message = None
    bible_data = None
    books = None
    chapters = None

    # Handle search query
    if search_query:
        try:
            # Parse the search query (e.g., "Genesis 1:1" or "Psalms 23")
            parts = search_query.split()
            book = parts[0]
            if len(parts) > 1:
                chapter_and_verse = parts[1].split(":")
                chapter = chapter_and_verse[0]
                if len(chapter_and_verse) > 1:
                    verse = chapter_and_verse[1]
        except (IndexError, ValueError):
            error_message = "Invalid search query. Use the format 'Book Chapter:Verse' (e.g., 'Genesis 1:1')."

    # Load books based on the selected testament
    if testament == "Old Testament":
        books = OLD_TESTAMENT_BOOKS
    elif testament == "New Testament":
        books = NEW_TESTAMENT_BOOKS

    # Load chapters based on the selected book
    if book and books:
        chapters = range(1, books.get(book, 0) + 1)

    # Fetch the requested data if chapter and verse are provided
    if book and chapter:
        try:
            chapter = int(chapter)
            if chapter <= 0 or (books and chapter > books.get(book, 0)):
                raise ValueError("Invalid chapter number.")
            if verse:
                verse = int(verse)
                if verse <= 0:
                    raise ValueError("Invalid verse number.")
        except ValueError as e:
            error_message = str(e)

        if not error_message:
            bible_data = fetch_bible_data(book, chapter, verse)
            if isinstance(bible_data, str) and bible_data.startswith("Error"):
                error_message = bible_data

    return render(request, 'accounts/bible_view.html', {
        'testament': testament,
        'book': book,
        'chapter': chapter,
        'verse': verse,
        'bible_data': bible_data,
        'books': books,
        'chapters': chapters,
        'error_message': error_message,
        'search_query': search_query
    })