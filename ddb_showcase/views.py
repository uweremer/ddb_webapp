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
            'title': 'Zusammenfassung - Bürgerbetieligung in Baden-Württemberg',
            'year':datetime.now().year,
        }
    )

def jugendbeteiligung(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'ddb_showcase/jugendbeteiligung.html',
        {
            'title': 'Kinder- und Jugendbeteiligung in Baden-Württemberg',
            'year':datetime.now().year,
        }
    )