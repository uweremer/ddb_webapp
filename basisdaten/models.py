from django.db import models
from django.db.models import Max

# Create your models here.


class Nur_BW_Gemeinden_Manager(models.Manager):
    """
    Manager um Ba-Wü Gemeinden zu filtern.

    Dieser Manager zum Modell `Gebietseinheit`` filtert nach Bundesland über
    die Variable `land` das Merkmal ``08`` (Baden-Württemberg), sowie über 
    die Variable ``textkennzeichen`` das Merkmal ``60`` (Gemeinde).
    """

    def get_queryset(self):
        return super(Nur_BW_Gemeinden_Manager, self).get_queryset().filter(land='08').filter(satzart='60')


class Gebietseinheit(models.Model):
    """
    Diese Klasse ist ein Modell, dass Gebietseinheiten beschreibt.

    Diese Klasse ist ein Modell, dass die Gebietseinheiten Kommunen, Kreise
    und Budesländer beschreibt. Die Daten stammen aus dem amtlichen 
    Gemeindeverzeichnis für Deutschland, das beim `Statistischen Bundesamt 
    <https://www.destatis.de/DE/ZahlenFakten/LaenderRegionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugQ/AuszugGV1QAktuell.html>`_
    verfügbar ist.

    Damit die Daten immer wahr bleiben, darf kein Eintrag überschrieben 
    werden, stattdessen muss bei Änderungen ein neuer Eintrag hinzugefügt 
    werden (die Variable ``Stand`` beinhaltet den Zeitpunkt des Standes).

    Zu dieser Klasse gibt es zwei Custom-Manager. Erstens den 
    ``BW_Gebietseinheiten_Manager``, um nur baden-württembergische Kommunen 
    ausgebeben zu lassen. Sie werden ``bw_objects`` aufgefrufen. Und den 
    ``Nur_BW_Gemeinden_Manager``, mit dem nur Gebietseinheiten ausgegeben werden,
    bei denen es sich um eine Gemeinde (in Ba-Wü) handelt. Sie werden mit 
    ``gde_objects`` aufgerufen.
    """

    SATZART_CHOICE = (
        ('10', 'Bundesland'),
        ('20', 'Regierungsbezirk'),
        ('30', 'Region'),
        ('40', 'Kreis'),
        ('50', 'Gemeindeverband'),
        ('60', 'Gemeinde'),
        )
    TEXTKENNZEICHEN_CHOICE = (
        ('41', 'Kreisfreie Stadt'),
        ('42', 'Stadtkreis (nur in Baden-Württemberg)'),
        ('43', 'Kreis'),
        ('44', 'Landkreis'),
        ('45', 'Regionalverband (nur im Saarland)'),
        ('50', 'Verbandsfreie Gemeinde'),
        ('51', 'Amt'),
        ('52', 'Samtgemeinde'),
        ('53', 'Verbandsgemeinde'),
        ('54', 'Verwaltungsgemeinschaft '),
        ('55', 'Kirchspielslandgemeinde'),
        ('56', 'Verwaltungsverband'),
        ('58', 'Erfüllende Gemeinde'),
        ('60', 'Markt'),
        ('61', 'Kreisfreie Stadt'),
        ('62', 'Stadtkreis (nur in Baden-Württemberg)'),
        ('63', 'Stadt'),
        ('64', 'Kreisangehörige Gemeinde'),
        ('65', 'gemeindefreies Gebiet-bewohnt'),
        ('66', 'gemeindefreies Gebiet-unbewohnt'),
        ('67', 'Große Kreisstadt'),
        )
    VERSTAEDTERUNG_CHOICE = (
        ('1', 'Stadt'),
        ('2', 'Kleinere Stadt oder Vorort'),
        ('3', 'ländliches Gebiet'),
        )
    regionalschluessel = models.CharField(max_length=12, blank=False, help_text="12-stelliger amtlicher Regionalschlüssel") 
    satzart =  models.CharField(max_length=2, blank=False, choices=SATZART_CHOICE, help_text="Politische Ebene")
    textkennzeichen =  models.CharField(max_length=2, blank=True, choices=TEXTKENNZEICHEN_CHOICE, help_text="Bezeichnung der kommunalen Einheit")
    land = models.CharField(max_length=2, blank=False, help_text="Bundesland-Schlüssel")
    regierungsbezirk = models.CharField(max_length=1, blank=True, help_text="Regierungsbezirks-Schlüssel")
    kreis = models.CharField(max_length=2, blank=True, help_text="Kreis-Schlüssel")
    gemeindeverband = models.CharField(max_length=4, blank=True, help_text="Gemeindeverband-Schlüssel")
    gemeinde = models.CharField(max_length=3, blank=True, help_text="Gemeinde-Schlüssel")
    name = models.CharField(max_length=50, blank=False, help_text="Name der Gebietseinheit")
    flaeche = models.DecimalField('Flaeche in km2', null=True, max_digits=5, decimal_places=2, help_text="Fläche in km2")
    bevoelkerung = models.IntegerField(null=True, help_text="Einwohnerzahl")
    bevolkerungsdichte = models.IntegerField(null=True, help_text="Einwohner pro km2")
    postleitzahl = models.CharField(max_length=5, blank=True, help_text="Postleitzahl des Verwaltungssitzes")
    longitude =  models.DecimalField(null=True, max_digits=9,decimal_places=7, help_text="Längengrad WGS84")
    latitude =  models.DecimalField(null=True, max_digits=9, decimal_places=7, help_text="Breitengrad WGS84")
    verstaedterung = models.CharField(max_length=1, blank=True, choices=VERSTAEDTERUNG_CHOICE, help_text="Grad der Verstädterung (nach Eurostat DEGURBA)")
    stand =  models.DateField(blank=False, help_text="Zeitpunkt des Standes des Eintrages")
    erstellt_am =  models.DateField(auto_now_add=True)

    
    objects = models.Manager() # The default manager.
    gde_objects = Nur_BW_Gemeinden_Manager() # Manager für baden-würrtembergische Gemeinden

    class Meta:
        verbose_name_plural = 'Gebietseinheiten'
        unique_together = (("regionalschluessel", "stand"),)

    def __str__(self):
        return '%s %s (RS: %s, ID: %s)' % (self.postleitzahl, self.name, self.regionalschluessel, self.pk)

class Gebietseinheit_Erweiterung(models.Model):
    """
    Diese Klasse ist ein Modell für Zusatzinfotmationen zu den Gebietseinheiten.
    
    Das Modell wird befüllt, wenn eine neuer Suchdurchlauf für die jeweilige
    Kommune initialisiert wird. Dabei wird über ein Formular abgefragt, mit 
    welcher Bezeichnung nach der Kommune gesucht werden soll.

    Zusätzlich werden Kontaktinformationen für jede Kommune und den Ansprech-
    partner eingetragen.

    Zudem wird zu der jeweiligen Kommune das Wappen hochgeladen.
    """
    ANREDE_CHOICE = (
        ('1', 'Herr'),
        ('2', 'Frau'),
        )
    gebietseinheit = models.ForeignKey(Gebietseinheit, on_delete=models.PROTECT, 
                                       limit_choices_to={'satzart': '60', 'land': '08'},
                                       help_text="Name der Kommune")
    ortsname_suche = models.CharField(max_length=100, verbose_name="Gemeindename für Suche", help_text='Gemeindename, so wie er im Webscraping gesucht werden soll')
    ansprechpartner_anrede = models.CharField(blank=True, max_length=1, choices=ANREDE_CHOICE)
    ansprechpartner_vorname = models.CharField(blank=True, max_length=100)
    ansprechpartner_name = models.CharField(blank=True, max_length=100)
    ansprechpartner_funktion = models.CharField(blank=True, max_length=100, verbose_name="Funktion Ansprechpartner", help_text='Bürgermeister, Hauptamstleiter, Stabstelle BB etc.')
    ansprechpartner_telefon = models.CharField(blank=True, max_length=20, verbose_name="Telefon Ansprechpartner")
    ansprechpartner_mail = models.EmailField(blank=True, max_length=100, verbose_name="E-Mail Ansprechpartner", help_text='Persönliche oder Funktions E-Mailadresse')
    strasse_gv = models.CharField(max_length=100, verbose_name="Straße und Hausnummer GV", help_text='Anschrift der Gemeindeverwaltung')
    plz_ort_gv = models.CharField(max_length=100, verbose_name="PLZ und Ort GV", help_text='Anschrift der Gemeindeverwaltung')
    homepage_gv = models.CharField(blank=True, max_length=100, verbose_name="Homepage GV", help_text='Offizielle Homepage der Gemeinde')
    mail_gv = models.EmailField(blank=True, verbose_name="E-Mail GV", help_text='allg. E-Mail der Gemeindeverwaltung')
    wappen = models.FileField(blank=True, upload_to='wappen/', help_text='Wappen der Kommune als .png in Auflösung 140px x 142px')
    erstellt_am =  models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Gebietseinheiten Erweiterung'

    def __str__(self):
        return '%s' % (self.gebietseinheit)


    
class Bearbeitungsstand(models.Model):
    """
    Diese Klasse ist ein Modell für den Bearbeitungsstand einer Kommune.
    
    Dieses Modell speichert den aktuellen Bearbeitungsstatus der Kommunen. Für 
    jede Kommune wird ein Ersteintrag mit dem Status 0-unbearbeitet angelegt. 
    Jede Änderung des Bearbeitungstatus generiert einen neuen Eintrag für die 
    Kommune.

    Das Modell dokumentiert somit den Zeitpunkte der jeweiligen Statusänderung. 
    Auf das Modell wird zugegriffen durch [XXX], um die nächste zu bearbeitende 
    Kommune auszuwählen.
    """

    BEARBEITUNGSSTAND_CHOICE = (
        ('0', 'unbearbeitet'),
        ('1', 'Rohtreffer generiert'),
        ('2', 'Rohtreffer bereinigt'),
        ('3', 'Kodierauftrag zugeteilt'),
        ('4', 'Rohtreffer kodiert'),
        ('5', 'Treffer aufbereitet'),
        ('6', 'Ergebnisse veröffentlicht'),
        ('7', 'Ergebnisse in ext. Prüfung'),
        ('8', 'Ergebnisse geprüft'),
        )
    gebietseinheit = models.ForeignKey(Gebietseinheit, on_delete=models.PROTECT, 
                                       limit_choices_to={'satzart': '60', 'land': '08'},
                                       help_text="Name der Kommune")
    bearbeitungsstand =  models.CharField(max_length=1, choices=BEARBEITUNGSSTAND_CHOICE, default='0',
                                          help_text="Bearbeitungsstand der Kommune")
    erstellt_am =  models.DateField(auto_now_add=True)

    objects = models.Manager() # The default manager.


    class Meta:
        verbose_name_plural = 'Bearbeitungsstand'
        unique_together = (("gebietseinheit", "bearbeitungsstand"),)
        get_latest_by = 'erstellt_am'

    def __str__(self):
        return 'ID: %s %s Stand: %s' % (self.id, self.gebietseinheit, self.bearbeitungsstand)
 
def bearbeitungsstand_max(bearbeitungsstand_query):
    """
        
    """

    alle=list(set(bearbeitungsstand_query.values_list('gebietseinheit', flat=True)))
    fre_bearbeitungsstand=[]
    for i in alle:
        b=bearbeitungsstand_query.filter(gebietseinheit=i)
        c=b.aggregate(Max('bearbeitungsstand'))
        d=b.get(bearbeitungsstand=c.get('bearbeitungsstand__max')).gebietseinheit_id
        fre_bearbeitungsstand.append({'gebietseinheit': d, 'bearbeitungsstand_max': c.get('bearbeitungsstand__max')})        
    
    bearbeitungsstand_0=[]    
    bearbeitungsstand_1=[]
    bearbeitungsstand_2=[]
    bearbeitungsstand_3=[]
    bearbeitungsstand_4=[]
    bearbeitungsstand_5=[]
    bearbeitungsstand_6=[]
    bearbeitungsstand_7=[]

    for item in fre_bearbeitungsstand:
        if item['bearbeitungsstand_max']=='0':
            bearbeitungsstand_0.append(item['gebietseinheit'])
        if item['bearbeitungsstand_max']=='1':
            bearbeitungsstand_1.append(item['gebietseinheit'])
        if item['bearbeitungsstand_max']=='2':
            bearbeitungsstand_2.append(item['gebietseinheit'])
        if item['bearbeitungsstand_max']=='3':
            bearbeitungsstand_3.append(item['gebietseinheit'])
        if item['bearbeitungsstand_max']=='4':
            bearbeitungsstand_4.append(item['gebietseinheit'])
        if item['bearbeitungsstand_max']=='5':
            bearbeitungsstand_5.append(item['gebietseinheit'])
        if item['bearbeitungsstand_max']=='6':
            bearbeitungsstand_6.append(item['gebietseinheit'])
        if item['bearbeitungsstand_max']=='7':
            bearbeitungsstand_7.append(item['gebietseinheit'])

    bearbeitungsstand_liste_0 = bearbeitungsstand_query.filter(bearbeitungsstand=0).filter(gebietseinheit__in=bearbeitungsstand_0)
    bearbeitungsstand_liste_1 = bearbeitungsstand_query.filter(bearbeitungsstand=1).filter(gebietseinheit__in=bearbeitungsstand_1)
    bearbeitungsstand_liste_2 = bearbeitungsstand_query.filter(bearbeitungsstand=2).filter(gebietseinheit__in=bearbeitungsstand_2)
    bearbeitungsstand_liste_3 = bearbeitungsstand_query.filter(bearbeitungsstand=3).filter(gebietseinheit__in=bearbeitungsstand_3)
    bearbeitungsstand_liste_4 = bearbeitungsstand_query.filter(bearbeitungsstand=4).filter(gebietseinheit__in=bearbeitungsstand_4)
    bearbeitungsstand_liste_5 = bearbeitungsstand_query.filter(bearbeitungsstand=5).filter(gebietseinheit__in=bearbeitungsstand_5)
    bearbeitungsstand_liste_6 = bearbeitungsstand_query.filter(bearbeitungsstand=6).filter(gebietseinheit__in=bearbeitungsstand_6)
    bearbeitungsstand_liste_7 = bearbeitungsstand_query.filter(bearbeitungsstand=7).filter(gebietseinheit__in=bearbeitungsstand_7)
    bearbeitungsstand_max=[bearbeitungsstand_liste_0, bearbeitungsstand_liste_1, bearbeitungsstand_liste_2, 
                            bearbeitungsstand_liste_3, bearbeitungsstand_liste_4, bearbeitungsstand_liste_5,
                            bearbeitungsstand_liste_6, bearbeitungsstand_liste_7]

    return(bearbeitungsstand_max)
