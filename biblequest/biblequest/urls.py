from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Accounts app URLs
    path('', CustomLoginView.as_view(), name='root'),  # Default root URL redirects to login page
]
