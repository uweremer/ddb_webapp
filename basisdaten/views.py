from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
# Create your views here.


def basisdaten(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'basisdaten/index.html',
        {
            'title': 'Basisdaten',
            'year':datetime.now().year,
            'nbar': 'basisdaten',
        }
    )

