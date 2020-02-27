"""
Definition der Datenbank-Modelle für die **Beteiligungsverfahren**
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Partial Date: https://stackoverflow.com/questions/30134526/date-conveniences-validation-display-etc-for-partial-dates-in-django


class BeteiligungsEintrag(models.Model):
    """
    Diese Klasse ist ein Modell, dass Beteiligungsereignisse beschreibt.

    """

    PARTIAL_YEAR='%Y'
    PARTIAL_MONTH='%Y-%m'
    PARTIAL_DAY='%Y-%m-%d'
    PARTIAL_CHOICES = (
      (PARTIAL_YEAR, 'Jahr'),
      (PARTIAL_MONTH, 'Monat'),
      (PARTIAL_DAY, 'Tag'),
    )

    TREFFER_ART_CHOICE = (
        ('1', 'Ankündigung oder Einladung'),
        ('2', 'Bericht oder Zeitungsbericht'),
        ('3', 'Webseite zum Beteiligungsverfahren '),
        ('9', 'Sonstiges'),
        )
    EBENE_CHOICE = (
        ('1', 'Kommunale Ebene'),
        ('2', 'Kommunale Ebene (mehrere Kommunen)'),
        ('3', '(Land-)Kreis-Ebene'),
        ('4', 'regionale Ebene'),
        ('5', 'Landes-Ebene'),
        ('6', 'Bundes-Ebene'),
        ('7', 'europäische Ebene'),
        ('9', 'Sonstiges')
        )
    THEMENGEBIET_CHOICE = (
        ('01', 'Infrastruktur'),
        ('02', 'Keine Festlegung'),
        ('03', 'Umwelt / Energie'),
        ('04', 'Jugend, Soziales, Sport'),
        ('05', 'Mobilität / Verkehr'),
        ('06', 'Bürgerbeteiligung'),
        ('07', 'Finanzen'),
        ('08', 'Migration'),
        ('09', 'Kultur / Bildung'),
        ('10', 'Wirtschaft'),
        ('11', 'Sonstiges'),
        ('12', 'Stadtentwicklung')
        )
    ZIELGRUPPE_CHOICE = (
        ('1', 'Bürger allg. / undefiniert'),
        ('2', 'Anwohner'),
        ('3', 'Betroffene'),
        ('4', 'Kinder, Jugendliche, Schüler'),
        ('5', 'Senioren, Ältere'),
        ('6', 'Migranten'),
        ('7', 'Andere'),
        )
    INITIATOR_CHOICE = (
        ('1', 'Kommunalverwaltung oder Bürgermeister'),
        ('2', 'Behörde oder Amt (nicht Kommunal)'),
        ('3', 'Gemdeinderat, Stadtrat'),
        ('4', 'Partei'),
        ('5', 'Bürgerinitiative'),
        ('6', 'Verband oder Verein'),
        ('7', 'Einzelperson'),
        ('8', 'Unternehmen'),
        ('9', 'Unbekannt / Andere'),
        )
    VALIDIERUNGS_CHOICE = (
        ('not', 'ungeprüfte Rohdaten'),
        ('na1', 'Name in Bezeichnung'),
        ('na1', 'Name in Beschreibung'),
        ('int', 'intern geprüft'),
        ('ext', 'in externer validierung'),
        ('val', 'extern validiert'),
        )

    #kodierauftrag = models.IntegerField()
    gebietseinheit = models.ForeignKey('basisdaten.Gebietseinheit', on_delete=models.PROTECT, 
                                       limit_choices_to={'satzart': '60', 'land': '08'},
                                       help_text="Name der Kommune (sortiert nach Regionalschluessel)")
    #rohtreffer = models.IntegerField()
    andere_rohtreffer = models.CharField(max_length=100, help_text="Doppelte Rohtreffer könenn Sie hier mit KOMMA getrennt eintragen", blank=True, null=True)
    alternative_quelle= models.BooleanField(help_text="Falls die Quelle nicht der eigentliche Rohtreffer war, sondern Sie durch weiterklicken zum Treffer gelangt sin, können Sie hier den eigentlichen Link einfügen, auf dem Sie die Informationen gefunden haben.")
    link_alternative_quelle = models.URLField(max_length=600, blank=True, help_text="Link zur alternativen Quelle")
    treffer_art = models.CharField(max_length=1, verbose_name="Art des Treffers", choices=TREFFER_ART_CHOICE)

    bezeichnung = models.TextField(max_length=150, blank=False, help_text="Wie wird das Beteiligungsverfahren genannt?")
    beschreibung = models.TextField(max_length=1500, blank=False, help_text="Kurzbeschreibung des Beteiligungsverfahrens: Wer, was, wie und warum? (z.B. copy+paste von Webseite)")

    themengebiet =  models.CharField(max_length=2, choices=THEMENGEBIET_CHOICE, help_text="Welches ist das wichtigste Themengebiet")
    weiteres_themengebiet =  models.CharField(max_length=2, choices=THEMENGEBIET_CHOICE, help_text="Gibt es ein weiteres *zentrales* Themengebiet", blank=True, null=True)
    zielgruppe = models.CharField(max_length=1, choices=ZIELGRUPPE_CHOICE, help_text="An wen richtet sich das Beteiligungsverfahren?")
    ebene_zielgruppe = models.CharField(max_length=1,choices=EBENE_CHOICE, help_text="Aus welcher Ebene rekrutieren sich die beteiligten Bürger?")
    initiator = models.CharField(max_length=1,choices=INITIATOR_CHOICE, help_text="Wer hat das Beteiligungsverfahren initiiert")

    start_datum =  models.DateField(blank=False, help_text="Wenn nicht genau bekannt, bitte 'runden' (z.B. 1.7.2017 für Juli 2017)")
    unscharfes_datum = models.CharField('Datum genau auf', choices=PARTIAL_CHOICES, max_length=10,  help_text="Bitte hier angeben für welchen Datumsbereich das Datum gilt")
    end_datum = models.DateField(blank=True, null=True, help_text="Enddatum nur angeben, wenn das Verfahren mehr als einen Tag dauert")
    unscharfes_end_datum = models.CharField('End-Datum genau auf', blank=True, choices=PARTIAL_CHOICES, max_length=10)

    ansprechpartner_name = models.CharField(max_length=50, blank=True, help_text="Initiator / Ansprechpartner wenn bekannt, sonst nur unten Institution angeben")
    ansprechpartner_funktion = models.CharField(max_length=50, blank=True, help_text="Wenn bekannt (z.B. 'Bürgermeister')")
    ansprechpartner_email= models.EmailField(blank=True, help_text="Wenn bekannt")
    ansprechpartner_institution = models.CharField(max_length=255, blank=False, help_text="Bitte genau aungeben, z.B.: 'Grünflächenamt Stadt XYZ' oder 'Bürgerinitiative Windkraft e.v.'")
    
    weitere_dokumentation = models.URLField(blank=True, max_length=600, help_text = "Weblink zu weiterer Dokumentation (z.B. Protokolle, Webseiten etc.).")
    weitere_dokumentation_zusatzfeld_1 = models.URLField(blank=True, max_length=600, help_text = "Weblink zu weiterer Dokumentation (z.B. Protokolle, Webseiten etc.).")
    weitere_dokumentation_zusatzfeld_2 = models.URLField(blank=True, max_length=600, help_text = "Weblink zu weiterer Dokumentation (z.B. Protokolle, Webseiten etc.).")

    kommentar = models.TextField(blank=True, max_length=300, help_text = "Hier können Sie Anmerkungen zur Kodierung hinterlassen")
    validierungstatus = models.CharField(default='not', choices=VALIDIERUNGS_CHOICE, max_length=3)

    #bearbeiter = models.IntegerField()
    stand =  models.DateField(auto_now=True, help_text="Wird automatisch eingetragen")
    erstellt_am =  models.DateField(auto_now_add=True, help_text="Wird automatisch eingetragen")

   
    class Meta:
        abstract = True


class Beteiligungsereignis_Abstract(BeteiligungsEintrag):
    """
    Diese Klasse beschreibt Beteiligungsereignisse.

    Die Klasse erweitert die Base-Klasse BeteiligungsEintrag um Ereignis-spezifische Variablen.
    """

    EBENE_CHOICE = (
        ('1', 'Kommunale Ebene)'),
        ('2', 'Kommunale Ebene (mehrere Kommunen)'),
        ('3', '(Land-)Kreis-Ebene'),
        ('4', 'regionale Ebene'),
        ('5', 'Landes-Ebene'),
        ('6', 'Bundes-Ebene'),
        ('7', 'europäische Ebene'),
        ('9', 'Sonstiges')
        )
    METHODE_CHOICE = (
        ('01', 'Informationsveranstaltung'),
        ('02', 'Workshop, Bürger-, Planungs-, Strategie-, Bilanzwerkstatt'),
        ('03', 'Bürgerforum, Stadtteilforum'),
        ('04', 'Bürgerdialog, Bürgercafé'),
        ('05', 'Umfrage, Befragung, Interviews (online/offline)'),
        ('06', 'Diskussionsveranstaltung'),
        ('07', 'Einwohnerversammlung, Bürgerversammlung'),
        ('08', 'Zukunftskonferenz, Zukunftswerkstatt'),
        ('09', 'Fokusgruppe'),
        ('10', 'World Cafe'),
        ('11', 'Kinder-/Jugendforum, -konferenz, -versammlung, -hearing, -werkstatt'),
        ('12', 'Planauslegung'), 
        ('20', 'Arbeitskreis, Arbeitsgruppe'),
        ('21', 'Stadtteilkonferenz, Bürgerkonferenz'),
        ('22', 'Bürgertisch'),
        ('23', 'Orts-, Nachbarschafts-, Stadteil-, Baustellen, / -begehung, -termin, -rundgang, -spaziergang, Bustour'),
        ('24', 'Runder Tisch'),
        ('25', 'Unterschriftensammlung'),
        ('26', 'Petition'),
        ('27', 'Austausch, Gesprächsrunde, Fragerunde, Sprechstunde'),
        ('28', 'Abschluss- oder Auftaktveranstaltung'),
        ('29', 'Bürgerrat, Bürgerpanel (Zufallsauswahl)'),
        ('30', 'Onlinebeteiligung'),
        ('31', 'Online-Petition'),
        ('70', 'Planfeststellungsverfahren, Stellungnahmen, Einwendung, Erörterung'),  
        ('81', 'Bürgerbegehren'),
        ('82', 'Bürgerentscheid'),
        ('83', 'Einwohnerantrag'),
        ('84', 'Volksbegehren'),
        ('85', 'Volksentscheid'),
        ('97', 'FEHLEINTRAG: XX'),
        ('98', 'FEHLEINTRAG: BE'),
        ('99', 'Andere, und zwar...'),
        )
    BETEILIGUNG_ART_CHOICE = (
        ('0', 'noch nicht kodiert'),
        ('1', 'Art 1'),
        ('2', 'Art 2'),
        ('3', 'Art 3'),
        ('9', 'unklar'),
        )

    sachfrage = models.TextField(max_length=250, blank=False, help_text="Wie lautet die Sachfrage, um die es geht (bitte als Frage formulierern, z.B.: 'Sollen im Ort zwei Windräder gebaut werden?' oder 'Wie soll der Marktplatz umgestaltet werden?'")
    ebene_sachfrage =  models.CharField(max_length=1, choices=EBENE_CHOICE, help_text="Auf welcher politisch-administrativen Ebene wird die Sachfrage entschieden?")
    
    beteiligungsprozess =  models.ForeignKey('Beteiligungsprozess', on_delete=models.PROTECT,
                                       help_text="Ist das Beteiligungsereignis Teil eines größeren Beteiligungsprozesses? Welcher (Prozess muss zuerst angelegt werden)?",
									   blank=True, null=True)
    
    methode = models.CharField(max_length=2,choices=METHODE_CHOICE, help_text="Welche Methode wird genutzt")
    andere_methode = models.CharField(blank=True, max_length=50, help_text="Andere, und zwar...")
    anzahl_teilnehmer = models.CharField(blank=True, max_length=50, help_text="Qualitativ: bitte wie in Quelle anggeben ('etwa 30', 'über 50' oder 'rund ein Dutzend'")
    anzahl_teilnehmer_quantifiziert = models.IntegerField(blank=True, null=True, help_text="Quantitativ: bitte als mindest-Anzahl angeben ('Dutzend' = 12, 'über 50' = 50, 'rund 300' =300)")
    formell = models.BooleanField(help_text="Handelt es sich um ein gesetzlich vorgeschriebenes Verfahren oer folgt es gesetzlich vorgeschriebenen Abläufen (z.B. Bürgerentscheid)")
    online_komponente = models.BooleanField(help_text="Gibt es eine Online-Komponente?")
    zufallsauswahl = models.NullBooleanField(help_text="Gibt es eine (teilweise) Zufallsauswahl der Bürger?")
    entscheidung = models.TextField(blank=True, max_length=1000, help_text="Gab/Gibt es ein Ergebnis der Beteiligung? Wie sieht das aus? Wann wurde das umgesetzt? Etc.")

    art_der_beteiligung = models.CharField(max_length=1, verbose_name="Art der Beteiligung", choices=BETEILIGUNG_ART_CHOICE, default=0, help_text = "Kodieren auf Basis der Beschreibung")


    objects = models.Manager() # The default manager.

    class Meta:
        abstract = True 


class Beteiligungsereignis(Beteiligungsereignis_Abstract):
    class Meta:
        verbose_name_plural = 'Beteiligungsereignisse'
        #unique_together = (("regionalschluessel", "stand"),)

    def __str__(self):
        return '%s - %s, Start: %s' % (self.gebietseinheit, self.bezeichnung, self.start_datum)



class Beteiligungsprozess_Abstract(BeteiligungsEintrag):
    """
    Diese Klasse ist ein Modell, dass Beteiligungsprozesse beschreibt.

    Prozesse bestehen aus mehreren Béteiligungsereignissen zur selben
    übergeordneten Sachfrage.
    """

    EBENE_CHOICE = (
        ('1', 'Kommunale Ebene)'),
        ('2', 'Kommunale Ebene (mehrere Kommunen)'),
        ('3', '(Land-)Kreis-Ebene'),
        ('4', 'regionale Ebene'),
        ('5', 'Landes-Ebene'),
        ('6', 'Bundes-Ebene'),
        ('7', 'europäische Ebene'),
        ('9', 'Sonstiges')
        )
    
    sachfrage = models.TextField(max_length=250, blank=False, help_text="Wie lautet die Sachfrage, um die es geht (bitte als Frage formulierern, z.B.: 'Sollen im Ort zwei Windräder gebaut werden?' oder 'Wie soll der Marktplatz umgestaltet werden?'")
    ebene_sachfrage =  models.CharField(max_length=1, choices=EBENE_CHOICE, help_text="Auf welcher politisch-administrativen Ebene wird die Sachfrage entschieden?")

    entscheidung = models.TextField(blank=True, max_length=1000, help_text="Gab/Gibt es ein Ergebnis des Beteiligungsprozesses? Wie sieht das aus? Wann wurde das umgesetzt? Etc.")


    objects = models.Manager() # The default manager.

    class Meta:
        abstract = True 
        

class Beteiligungsprozess(Beteiligungsprozess_Abstract):
    class Meta:
        verbose_name_plural = 'Beteiligungsprozesse'

    def __str__(self):
        return '%s - %s' % (self.gebietseinheit.name, self.bezeichnung)




class Dauereinrichtung_Abstract(BeteiligungsEintrag):
    """
    Diese Klasse ist ein Modell, dass Dauereinrichtung beschreibt.
    """

    anzahl_teilnehmer = models.CharField(blank=True, max_length=50, help_text="Bitte wie in Quelle anggeben (z.B. 'etwa 30', oder 'über 50' oder 'rund ein Dutzend'")

    
    objects = models.Manager() # The default manager.
    
    class Meta:
        abstract = True 


class Dauereinrichtung(Dauereinrichtung_Abstract):

    class Meta:
        verbose_name_plural = 'Dauereinrichtungen'

    def __str__(self):
        return '%s - %s' % (self.gebietseinheit, self.bezeichnung)




    
class Suchanfrage(models.Model):
    """
    Diese Klasse ist ein Modell, dass Suchanfragen loggt.

    """

    querystring = models.CharField(max_length=100, help_text="Suchanfrage", blank=True, null=True)
    results = models.IntegerField(blank=True, null=True, help_text="Anzahl der angezeigten Treffer")
    date_of_query =  models.DateField(auto_now_add=True, help_text="Datum der Suchanftrage wird automatisch eingefügt")
   
    class Meta:
        verbose_name_plural = 'Suchanfragen'

    def __str__(self):
        return '%s, %s' % (self.querystring, self. results)