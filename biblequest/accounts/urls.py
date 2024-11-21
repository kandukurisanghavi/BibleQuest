# accounts/urls.py

from django.urls import path
from .views import CustomLoginView, register, home, quiz, verse_of_the_day, logout_view

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),  # Root URL for login page
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('quiz/', quiz, name='quiz'),
    path('verse_of_the_day/', verse_of_the_day, name='verse_of_the_day'),
    path('logout/', logout_view, name='logout'),
]