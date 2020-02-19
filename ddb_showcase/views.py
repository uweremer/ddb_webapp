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
            'title': 'Zusammenfassung - Bürgerbeteiligung in Baden-Württemberg',
            'year':datetime.now().year,
            'nbar': 'zusammenfassung',
        }
    )

def dialogbeteiligung(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'ddb_showcase/dialogbeteiligung.html',
        {
            'title': 'Dialogorientierte Bürgerbeteiligung in Baden-Württemberg',
            'year':datetime.now().year,
            'nbar': 'dialogbeteiligung',
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
            'nbar': 'jugendbeteiligung',
        }
    )

from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader # um Templates zu laden
from datetime import datetime
from django.http import Http404
from django.template import loader # um Templates zu laden


from basisdaten.models import Gebietseinheit
from basisdaten.models import Bearbeitungsstand
from basisdaten.models import Gebietseinheit_Erweiterung
from ddb_showcase.models import Beteiligungsereignis, Beteiligungsprozess, Dauereinrichtung


from django.db.models import Count, Max

# Create your views here.


def beteiligungsverfahren(request):
    return render(
        request,
        'ddb_showcase/index2.html',
        {
            'title':'Gefundene Beteiligungsverfahren',
            'year':datetime.now().year,
        }
    )

from django.utils import timezone
from django.views.generic.list import ListView

class GemeindeListView(ListView):
    model = Gebietseinheit
    paginate_by = 1103  # if pagination is desired
    queryset = Gebietseinheit.gde_objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

# Use Listviews: https://docs.djangoproject.com/en/1.11/topics/class-based-views/generic-display/


def gemeindeansicht(request, gebietseinheit_id): 
    #gebietseinheit_id=10195
    try:
        Bearbeitungsstand.objects.get(bearbeitungsstand=4, gebietseinheit_id = gebietseinheit_id)
    except Bearbeitungsstand.DoesNotExist:
        raise Http404("Keine Einträge vorhanden!")

    aktueller_bearbeitungsstand = int(Bearbeitungsstand.objects.filter(gebietseinheit_id = gebietseinheit_id).aggregate(Max('bearbeitungsstand'))['bearbeitungsstand__max'])

    #Für Infobox auf Webseite oben rechts:
    infobox = Gebietseinheit.objects.get(pk=gebietseinheit_id)
    infobox.kreisname = Gebietseinheit.objects.get(satzart='40', land='08', regierungsbezirk=infobox.regierungsbezirk, kreis=infobox.kreis).name
    infobox.landname = Gebietseinheit.objects.get(satzart='10', land='08').name
    infobox_erweiterung = Gebietseinheit_Erweiterung.objects.get(gebietseinheit=gebietseinheit_id)

    #Für Liste aller Beteiligungsereignisse der jeweiligen Kommune:
    beteiligungsereignisse = Beteiligungsereignis.objects.filter(gebietseinheit_id = gebietseinheit_id).order_by('-start_datum')
    beteiligungsprozesse = Beteiligungsprozess.objects.filter(gebietseinheit_id = gebietseinheit_id).order_by('-start_datum')
    dauereinrichtungen = Dauereinrichtung.objects.filter(gebietseinheit_id = gebietseinheit_id).order_by('-start_datum')

    beteiligungsprozesse = beteiligungsprozesse.annotate(Count('beteiligungsereignis'))

    infobox.anzahl_be = len(beteiligungsereignisse)
    infobox.anzahl_bp = len(beteiligungsprozesse) 
    infobox.anzahl_de = len(dauereinrichtungen) 

    bearbeitungsstand_datum = None
    
    context = {'infobox': infobox,
               'infobox_erweiterung': infobox_erweiterung,
               'beteiligungsereignisse': beteiligungsereignisse,
               'beteiligungsprozesse': beteiligungsprozesse,
               'dauereinrichtungen': dauereinrichtungen,
               'title': 'Gesamtübersicht',
               'aktueller_bearbeitungsstand': aktueller_bearbeitungsstand,
               'bearbeitungsstand_datum': bearbeitungsstand_datum,
               'year': datetime.now().year,}

    return render(request, 'ddb_showcase/gemeindeansicht.html', context)


def beteiligungsereignis(request, gebietseinheit_id, beteiligungsereignis_id):
    #beteiligungsprozess_id=5
    try:
        Beteiligungsereignis.objects.get(pk = beteiligungsereignis_id)
    except Beteiligungsereignis.DoesNotExist:
        raise Http404("Kein Beteiligungsereignis vorhanden!")

    beteiligungsereignis = Beteiligungsereignis.objects.get(pk = beteiligungsereignis_id)

    #Für Infobox auf Webseite oben rechts:
    infobox = Gebietseinheit.objects.get(pk=gebietseinheit_id)
    infobox.kreisname = Gebietseinheit.objects.get(satzart='40', land='08', regierungsbezirk=infobox.regierungsbezirk, kreis=infobox.kreis).name
    infobox.landname = Gebietseinheit.objects.get(satzart='10', land='08').name
    infobox_erweiterung = Gebietseinheit_Erweiterung.objects.get(gebietseinheit=gebietseinheit_id)

    bearbeitungsstand_datum = None


    context = {'infobox': infobox,
               'infobox_erweiterung': infobox_erweiterung,
               'beteiligungsereignis': beteiligungsereignis,
               'title': 'Beteiligungsereignis',
               'bearbeitungsstand_datum': bearbeitungsstand_datum,
               'year': datetime.now().year,}
    
    return render(request, 'ddb_showcase/beteiligungsereignis.html', context)


def beteiligungsprozess(request, gebietseinheit_id, beteiligungsprozess_id):
    #beteiligungsprozess_id=5
    try:
        Beteiligungsprozess.objects.get(pk = beteiligungsprozess_id)
    except Beteiligungsprozess.DoesNotExist:
        raise Http404("Kein Beteiligungsprozess vorhanden!")

    beteiligungsprozess = Beteiligungsprozess.objects.get(pk = beteiligungsprozess_id)
    beteiligungsereignisse = Beteiligungsereignis.objects.filter(beteiligungsprozess__pk = beteiligungsprozess_id).order_by('-start_datum')

    #Für Infobox auf Webseite oben rechts:
    infobox = Gebietseinheit.objects.get(pk=gebietseinheit_id)
    infobox.kreisname = Gebietseinheit.objects.get(satzart='40', land='08', regierungsbezirk=infobox.regierungsbezirk, kreis=infobox.kreis).name
    infobox.landname = Gebietseinheit.objects.get(satzart='10', land='08').name
    infobox_erweiterung = Gebietseinheit_Erweiterung.objects.get(gebietseinheit=gebietseinheit_id)

    bearbeitungsstand_datum = None


    context = {'infobox': infobox,
               'infobox_erweiterung': infobox_erweiterung,
               'beteiligungsprozess': beteiligungsprozess,
               'beteiligungsereignisse': beteiligungsereignisse,
               'title': 'Beteiligungsprozess',
               'bearbeitungsstand_datum': bearbeitungsstand_datum,
               'year': datetime.now().year,}

    
    return render(request, 'ddb_showcase/beteiligungsprozess.html', context)


def suf(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'ddb_showcase/suf.html',
        {
            'title': 'Scientific Use File',
            'year':datetime.now().year,
            'nbar': 'suf',
        }
    )
