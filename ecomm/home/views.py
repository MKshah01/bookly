from django.shortcuts import render

# Create your views here.
# home/views.py

from django.shortcuts import render

def home(request):
    # Add any context data you want to pass to the template
    return render(request, 'home/home.html')
