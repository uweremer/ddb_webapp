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
]