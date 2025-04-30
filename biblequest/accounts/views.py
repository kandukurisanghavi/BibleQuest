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
from django.core.paginator import Paginator
import json  # For parsing JSON data
from django.http import JsonResponse  # For returning JSON responses





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

from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
import json

def send_quiz_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            score = data.get('score')
            total_questions = data.get('total_questions')

            subject = "Your Quiz Results"
            from_email = 'biblequesta@gmail.com'
            to_email = [email]
            html_content = f"""
                <h3>Thank you for taking the quiz </h3>
                <p><strong> Your Score is :</strong> {score} out of {total_questions}</p>
            """

            email_message = EmailMultiAlternatives(subject, "Your quiz results are attached.", from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Email sending failed: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
        
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas

def download_quiz_results(request):
    score = request.GET.get('score', 0)
    total_questions = request.GET.get('total_questions', 0)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 800, "Quiz Results")
    pdf.drawString(100, 780, f"Score: {score} out of {total_questions}")
    pdf.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

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
    form_submitted = False
    success_message = None

    if request.method == 'POST':
        prayer_text = request.POST.get('prayer_request')
        category = request.POST.get('category')  # Get the selected category
        if prayer_text and category:
            PrayerRequest.objects.create(user=request.user, text=prayer_text, category=category)
            success_message = "Your prayer request has been submitted."
            form_submitted = True

    return render(request, 'accounts/prayer_request.html', {
        'form_submitted': form_submitted,
        'success_message': success_message,
    })


# View Prayer Requests (Prayer Wall)
from django.core.paginator import Paginator

@login_required
def view_prayer_requests(request):
    category = request.GET.get('category')  # Get the selected category from the query parameters
    if category:
        prayer_requests = PrayerRequest.objects.filter(category=category).order_by('-timestamp')
    else:
        prayer_requests = PrayerRequest.objects.all().order_by('-timestamp')

    paginator = Paginator(prayer_requests, 5)  # Paginate the prayer requests
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/view_prayer_requests.html', {
        'page_obj': page_obj,
        'selected_category': category,  # Pass the selected category to the template
    })
    
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
    testament = request.GET.get('testament')
    book = request.GET.get('book')
    chapter = request.GET.get('chapter')
    verse = request.GET.get('verse')
    search_query = request.GET.get('search')

    error_message = None
    bible_data = None
    books = None
    chapters = None
    total_chapters = 0

    if search_query:
        try:
            parts = search_query.split()
            book = parts[0]
            if len(parts) > 1:
                chapter_and_verse = parts[1].split(":")
                chapter = chapter_and_verse[0]
                if len(chapter_and_verse) > 1:
                    verse = chapter_and_verse[1]
        except (IndexError, ValueError):
            error_message = "Invalid search query. Use the format 'Book Chapter:Verse'."

    if testament == "Old Testament":
        books = OLD_TESTAMENT_BOOKS
    elif testament == "New Testament":
        books = NEW_TESTAMENT_BOOKS

    if book and books:
        chapters = range(1, books.get(book, 0) + 1)
        total_chapters = books.get(book, 0)

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
        'total_chapters': total_chapters,
        'error_message': error_message,
        'search_query': search_query
    })
