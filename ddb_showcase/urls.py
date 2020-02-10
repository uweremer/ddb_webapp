from django.contrib import admin
from django.urls import include, path
import ddb_showcase.views

urlpatterns = [
    path('', ddb_showcase.views.zusammenfassung, name='zusammenfassung'),
    path('zusammenfassung', ddb_showcase.views.zusammenfassung, name='zusammenfassung'),
    path('jugendbeteiligung', ddb_showcase.views.jugendbeteiligung, name='jugendbeteiligung'),
]
