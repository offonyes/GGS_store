from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path

from accounts_app.views import RegisterView, ProfileView
router = DefaultRouter()


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile')
]
