from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomLoginView, send_quiz_email  # Only import what you use

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Include app-level routes
    path('', CustomLoginView.as_view(), name='root'),  # Root route
]
