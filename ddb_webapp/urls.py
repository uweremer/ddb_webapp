"""ddb_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import baseapp.views


from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('', baseapp.views.home, name='home'),
    path('projekt', baseapp.views.projektbeschreibung, name='projektbeschreibung'),
    path('datenschutz', baseapp.views.datenschutz, name='datenschutz'),
    path('kontakt', baseapp.views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('auswertungen/', include('ddb_showcase.urls_auswertungen')),
    path('daten/', include('ddb_showcase.urls_daten')),
    path('basisdaten/', include('basisdaten.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)