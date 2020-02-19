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
            'title': 'Bürgerbeteiligung in Baden-Württemberg',
            'year':datetime.now().year,
            'nbar': 'home',
        }
    )

def projektbeschreibung(request):
    """Renders the Projektbeschreibungs page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'baseapp/projektbeschreibung.html',
        {
            'title': 'Projekt',
            'year':datetime.now().year,
            'nbar': 'projektbeschreibung',
        }
    )

def contact(request):
    """Renders the Kontakt page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'baseapp/contact.html',
        {
            'title': 'Kontakt',
            'year':datetime.now().year,
            'nbar': 'contact',
        }
    )
 
def datenschutz(request):
    """Renders the Datenschutz page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'baseapp/Datenschutz.html',
        {
            'title': 'Datenschutz',
            'year':datetime.now().year,
            'nbar': 'datenschutz',

        }
    )