from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime

# Create your views here.


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'baseapp/index.html',
        {
            'title': 'Startseite',
            'year':datetime.now().year,
        }
    )