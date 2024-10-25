# home/urls.py

from django.urls import path
from .views import home

urlpatterns = [
    path('home/', home, name="home"),  # Make sure the name is 'home'
]
