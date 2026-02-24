from django.urls import path

from .views import admin_dashboard, profile

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('dashboard/', admin_dashboard, name='admin-dashboard'),
]
