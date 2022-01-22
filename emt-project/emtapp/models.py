from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Django model Gebäude erstellen
class Building(models.Model):
    street_number = models.CharField('Strasse', max_length=100)
    city = models.CharField('Ort', max_length=100)
    BUILDING_TYPE_CHOICES = [
        ('EFH', 'Einfamilienhaus'),
        ('MFH', 'Mehrfamilienhaus'),
        ('GEW', 'Gewerbebau'),
        ]
    building_type = models.CharField('Gebäudeart', max_length=50, choices=BUILDING_TYPE_CHOICES, default='EFH')
    year_construction = models.DateField('Baujahr')
    ebf = models.IntegerField('Energiebezugsfläche [m2]')
    tenant = models.IntegerField('Anzahl Bewohner')
    HEATING_TYPE_CHOICES = [
        ('OHK', 'Ölheizkessel'),
        ('EHK', 'Erdgasheizkessel'),
        ('ESH', 'Elektro-Speicherheizung'),
        ('EZH', 'Elektro-Zentralheizung'),
        ('WPL', 'Wärmepumpe Luft-Wasser'),
        ('WPS', 'Wärmepumpe Sole-Wasser'),
        ]
    heating_type = models.CharField('Wärmeerzeugung', max_length=50, choices= HEATING_TYPE_CHOICES, default='OHK')
    DISTRIBUTION_TYPE_CHOICES = [
        ('HK', 'Heizkörper'),
        ('FB', 'Fussbodenheizung'),
        ]
    distribution_type = models.CharField('Wärmeabgabesystem', max_length=50, choices= DISTRIBUTION_TYPE_CHOICES, default='HK')
    HOTWATER_TYPE_CHOICES = [
        ('HG', 'Heizung ganzjährig'),
        ('HH', 'Heizung nur Heizperiode'),
        ('EL', 'Elektrisch'),
        ('WP', 'Wärmepumpenboiler'),
        ('SK', 'Solarkollektoren'),
        ]
    hotwater_type = models.CharField('Wassererwärmung', max_length=50, choices= HOTWATER_TYPE_CHOICES, default='HG')
    comment = models.TextField('Kommentar [-]', max_length=200, default='-')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Damit zum jeweiligen Gebäude der User hinzugefügt werden kann

    def __str__(self):
        return self.street_number

# Django model Zähler erstellen
class Counter(models.Model):
    name = models.CharField('Bezeichnung', max_length=100)  # Für Bezeichnung Zähler
    building = models.ForeignKey(Building, on_delete=models.CASCADE) # Ein Zähler kann nur in einem Haus verbaut sein, On-to-Many relationship
    #Auswahl der möglichen Zählertypen
    COUNTER_TYPE_CHOICES = [
        ('HLM', 'Heizölzähler Mechanisch'),
        ('HLP', 'Heizölzähler Pneumatisch'),
        ('HLD', 'Heizölzähler Digital'),
        ('EDG', 'Erdgaszähler'),
        ('SET', 'Stromzähler Einfachtarif'),
        ('SDT', 'Stromzähler Doppeltarif'),
        ]
    counter_type = models.CharField('Typ', max_length=50, choices= COUNTER_TYPE_CHOICES, default='EDG')
    conversion = models.FloatField('Wandlerfaktor', help_text= 'Heizöl: X[Lit/cm], X[Lit/%], 1[Lit], Erdgas 11.452 [kWh/m3], Strom 1[kWhel]', default=11.452)
    counter_overflow = models.BooleanField('Überlauf')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # Damit zum jeweiligen Zähler der User hinzugefügt werden kann

    def __str__(self):
        return self.name

# Django model Ablesung erstellen
class Readout(models.Model):
    #Verknüpfung mit User herstellen, damit nur dieser einen Ablesewert eingeben kann. --> UdemyKurs Todowoo Projekt?
    #Ein Zähler  hat mehrere Ablesungen, One-To-Many relationship
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    readout_date = models.DateField('Ablesedatum')  # Ablesedatum
    # register_1 = models.DecimalField('Zählerstand Register Nr.1', max_digits = 7, decimal_places=0) #Eingabewert beim Form einschränken
    # register_2 = models.DecimalField('Zählerstand Register Nr.2', max_digits = 7, decimal_places=0, default=0)
    register_1 = models.IntegerField('Zählerstand Register Nr.1', help_text='Werte ohne Komma eingeben')  # Eingabewert beim Form einschränken
    register_2 = models.IntegerField('Zählerstand Register Nr.2 (Nur wenn vorhanden)', default=0, help_text='Werte ohne Komma eingeben')
    comment = models.TextField('Kommentar [-]', max_length=200, default='-')
    energy_1 = models.IntegerField('Energie Register Nr.1 [kWh]')
    energy_2 = models.IntegerField('Energie Register Nr.2 [kWh]', default=0)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # Damit zur jeweiligen Ablesung der User hinzugefügt werden kann
    def __str__(self):
        return f'{self.counter}'  # Zahl in ein Zeichen String umwandeln, ansonsten ergibt sich ein Fehler

    # #Funktion um Zählerstand in Energie, vor Save, umzurechnen
    # def save(self, *args, **kwargs):
    #     energy_1 = models.IntegerField('Energieverbrauch Register Nr.1 [kWh]')
    #     energy_2 = models.IntegerField('Energieverbrauch Register Nr.2 [kWh]')
    #     #Zählerwert in Energie umrechnen
    #     #Der Energieträger muss berücksichtigt werden für Umrechnung Strom 1:1, Heizöl 10.5 kWh/dm3
    #     #Zählerstand Heizöl Pneumatisch dm3/%, Mechanisch dm3/cm, Digital dm3
    #     self.energy_1 = self.register_1 * 11.452
    #     self.energy_2 = self.register_2 * 11.452
    #     super(Readout, self).save(*args, **kwargs)
