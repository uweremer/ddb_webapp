from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime

# Create your views here.


def zusammenfassung(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'ddb_showcase/zusammenfassung.html',
        {
            'title': 'Zusammenfassung',
            'year':datetime.now().year,
        }
    )
