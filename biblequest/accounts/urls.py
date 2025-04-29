from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('select_difficulty/', views.select_difficulty, name='select_difficulty'),
    path('quiz/<str:difficulty>/', views.quiz, name='quiz'),
    path('send_quiz_email/', views.send_quiz_email, name='send_quiz_email'),
    path('verse_of_the_day/', views.verse_of_the_day, name='verse_of_the_day'),
    path('prayer_request/', views.prayer_request, name='prayer_request'),
    path('view_prayer_requests/', views.view_prayer_requests, name='view_prayer_requests'),
    path('add_comment/<int:prayer_request_id>/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('bible/', views.bible_view, name='bible_view'),
    path('download_quiz_results/', views.download_quiz_results, name='download_quiz_results'),
]
