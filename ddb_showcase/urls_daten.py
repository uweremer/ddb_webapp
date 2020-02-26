from django.contrib import admin
from django.urls import include, path, re_path
import ddb_showcase.views

from datetime import datetime
#import django.contrib.auth.views
from django.conf.urls import include
from ddb_showcase import views
from ddb_showcase import forms

urlpatterns = [
    path('suf', ddb_showcase.views.suf, name='suf'),
    path('beteiligungsverfahren', ddb_showcase.views.beteiligungsverfahren, name='beteiligungsverfahren'),
    path('gemeinden', ddb_showcase.views.GemeindeListView.as_view(), name='gemeindeliste'),
    path('gemeinden/<int:gebietseinheit_id>', ddb_showcase.views.gemeindeansicht, name='gemeindeansicht'),
    re_path(r'^(?P<gebietseinheit_id>[0-9]+)/beteiligungsereignis/(?P<beteiligungsereignis_id>[0-9]+)$', ddb_showcase.views.beteiligungsereignis, name='beteiligungsereignis'),
    re_path(r'^(?P<gebietseinheit_id>[0-9]+)/beteiligungsprozess/(?P<beteiligungsprozess_id>[0-9]+)$', ddb_showcase.views.beteiligungsprozess, name='beteiligungsprozess'),
    re_path(r'^durchsuchen/', views.SuchseiteView.as_view(form_class=forms.DateRangeSearchForm), name='suchseite')
]