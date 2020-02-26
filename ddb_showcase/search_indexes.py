import datetime
from haystack import indexes
from ddb_showcase.models import Beteiligungsereignis, Beteiligungsprozess
from basisdaten.models import Gebietseinheit

class BeteiligungsereignisIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    gebietseinheit = indexes.CharField(model_attr='gebietseinheit__name', boost=1.5)
    #author = indexes.CharField(model_attr='user')
    stand = indexes.DateTimeField(model_attr='stand')
    #content_auto = indexes.EdgeNgramField(model_attr='beschreibung') # for autocomplete

    def get_model(self):
        return Beteiligungsereignis

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(stand__lte=datetime.datetime.now()).filter(start_datum__gte=datetime.date(year=2015, month=1, day=1))

class BeteiligungsprozessIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author = indexes.CharField(model_attr='user')
    stand = indexes.DateTimeField(model_attr='stand')

    def get_model(self):
        return Beteiligungsprozess

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(stand__lte=datetime.datetime.now()).filter(start_datum__gte=datetime.date(year=2015, month=1, day=1))

class GebietseinheitIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Gebietseinheit

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(stand__lte=datetime.datetime.now()).filter(land='08').filter(satzart='60')






#Highlighting https://stackoverflow.com/a/13976447
#from haystack.query import SearchQuerySet
#from haystack.utils import Highlighter
#term = (u'Bürger')

#sqs = SearchQuerySet().filter(content=term)
#highlighter = Highlighter(term)
#print(highlighter.highlight(sqs[0].text))

#SearchQuerySet().autocomplete(content_auto='Them')[1].text