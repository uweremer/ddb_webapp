from django.contrib import admin
from django.urls import include, path
import basisdaten.views

urlpatterns = [
    path('', basisdaten.views.basisdaten, name='basisdaten'),
    #path('gebietseinheiten', basisdaten.views.gebietseinheiten, name='gebietseinheiten'),
]
