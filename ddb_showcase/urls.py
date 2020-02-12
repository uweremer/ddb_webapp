from django.contrib import admin
from django.urls import include, path, re_path
import ddb_showcase.views

from datetime import datetime
#import django.contrib.auth.views
from django.conf.urls import include
from . import views


urlpatterns = [
    path('', ddb_showcase.views.zusammenfassung, name='zusammenfassung'),
    path('zusammenfassung', ddb_showcase.views.zusammenfassung, name='zusammenfassung'),
    path('jugendbeteiligung', ddb_showcase.views.jugendbeteiligung, name='jugendbeteiligung'),
    path('dialogbeteiligung', ddb_showcase.views.dialogbeteiligung, name='dialogbeteiligung'),
    path('suf', ddb_showcase.views.suf, name='suf'),
    path('beteiligungsverfahren', ddb_showcase.views.beteiligungsverfahren, name='beteiligungsverfahren'),
    path('gemeinden', ddb_showcase.views.GemeindeListView.as_view(), name='gemeindeliste'),
    path('gemeinden/<int:gebietseinheit_id>', ddb_showcase.views.gemeindeansicht, name='gemeindeansicht'),
    re_path(r'^(?P<gebietseinheit_id>[0-9]+)/beteiligungsereignis/(?P<beteiligungsereignis_id>[0-9]+)$', ddb_showcase.views.beteiligungsereignis, name='beteiligungsereignis'),
    re_path(r'^(?P<gebietseinheit_id>[0-9]+)/beteiligungsprozess/(?P<beteiligungsprozess_id>[0-9]+)$', ddb_showcase.views.beteiligungsprozess, name='beteiligungsprozess'),
]