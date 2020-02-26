
from django import forms
from haystack.forms import HighlightedModelSearchForm


class DateRangeSearchForm(HighlightedModelSearchForm):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)


#data = {'q': 'Windenergie OR Windkraft', 'start_date': '2017-01-01', 'end_date': '2017-12-31'}
#a=DateRangeSearchForm(data)
#a.cleaned_data["q"]
#a.is_valid()
#a.cleaned_data["q"]

#sqs1 = a.searchqueryset.auto_query(a.cleaned_data["q"])
#sqs2 = a.searchqueryset.raw_search(a.cleaned_data["q"])
#len(sqs1)
#len(sqs2)

#sqs.result_class()