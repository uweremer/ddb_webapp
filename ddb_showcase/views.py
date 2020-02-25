from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from django.template import loader # um Templates zu laden
from django.views.generic.list import ListView
from datetime import datetime
from django.utils import timezone
from django.db.models import Count, Max
from django.db.models import Q
from haystack.generic_views import SearchView

from basisdaten.models import Gebietseinheit
from basisdaten.models import Bearbeitungsstand
from basisdaten.models import Gebietseinheit_Erweiterung
from ddb_showcase.models import Beteiligungsereignis, Beteiligungsprozess, Dauereinrichtung

# Static Pages
def zusammenfassung(request):
    """Renders the zusammenfassung page."""
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
    """Renders the dialogbeteiligung page."""
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
    """Renders the jugendbeteiligung page."""
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


def suf(request):
    """Renders the Sciebtific Use File page."""
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



def beteiligungsverfahren(request):
    return render(
        request,
        'ddb_showcase/index2.html',
        {
            'title':'Gefundene Beteiligungsverfahren',
            'year':datetime.now().year,
        }
    )


class GemeindeListView(ListView):
    """
    ListView aller Gemeinden mit Link auf die Gemeindeüberischt
    """
    model = Gebietseinheit
    paginate_by = 100  # if pagination is desired
    queryset = Gebietseinheit.gde_objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = datetime.now().year
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






from ddb_showcase import forms
from haystack.query import SearchQuerySet
class SuchseiteView(SearchView):
    """My custom search view."""

    template_name = './ddb_showcase/index.html'
    queryset = SearchQuerySet().all()
    form_class = forms.DateRangeSearchForm

    def get_queryset(self):
        queryset = super(SuchseiteView, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(SuchseiteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Daten durchsuchen'
        context['year'] = datetime.now().year
        context['nbar'] = 'suchseite'
        return context


#import simplejson as json
#from django.http import HttpResponse
#from haystack.query import SearchQuerySet
#def autocomplete(request):
#    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
#    suggestions = [result.title for result in sqs]
#    # Make sure you return a JSON object, not a bare list.
#    # Otherwise, you could be vulnerable to an XSS attack.
#    the_data = json.dumps({
#        'results': suggestions
#    })
#    return HttpResponse(the_data, content_type='application/json')