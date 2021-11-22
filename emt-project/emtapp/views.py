from django.shortcuts import render, redirect
from .models import Readout, Building, Counter
from .forms import CounterByUserForm, ReadoutForm, BuildingForm, CounterForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *

import logging

# Create your views here.
def home(request):
    return render(request, 'emtapp/home.html')


logger = logging.getLogger()
#####################
# AUTHENTIFIZIERUNG #
#####################
# Nutzer anmelden
def signup_user(request):
    if request.method == 'GET':
        # UserCreationForm anzeigen um neuen Nutzer zu erstellen
        return render(request, 'emtapp/signup_user.html', {'form': UserCreationForm()})
    else:
        # Prüfen ob beide Passwörter gleich sind
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Neues Objekt in Model User erzeugen
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)  # Neuen Nutzer einloggen
                return redirect('home')  # Mit view-Namen auf die Homepage weiterleiten

            except IntegrityError:  # Wenn es einen IntegrityError ergibt dann Fehlermeldung an Nutzer ausgeben
                return render(request, 'emtapp/signup_user.html',
                              {'form': UserCreationForm(), 'error': 'Dieser Nutzername existiert schon. Bitte neuen Nutzernamen wählen.'})
        else:
            # Wenn Passwörter nicht gepasst haben
            return render(request, 'emtapp/signup_user.html',
                          {'form': UserCreationForm(), 'error': 'Passwörter sind nicht gleich!'})

# Nutzer abmelden
@login_required
def logout_user(request):
    # Nur mit einem POST-Request machen, da Browser im Hintergrund alle href-Links sofort ladet.
    # Würde man die GET-Methode auch zulassen, wird der Browser den User sofort wieder ausloggen
    if request.method == 'POST':
        logout(request)  # Funktion aus Bibliothek django.contrib.auth
        return redirect('home')

# Nutzer einloggen
def login_user(request):
    if request.method == 'GET':
        # UserCreationForm anzeigen um neuen Nutzer zu erstellen
        return render(request, 'emtapp/login_user.html', {'form': AuthenticationForm()})
    else:
        # Achtung Input-Box Passwort ist nur noch password, nicht mehr password1
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            # Wenn Benutzer nicht vorhanden ist
            return render(request, 'emtapp/login_user.html', {'form': AuthenticationForm(), 'error':'Benutzername und Passwort stimmten nicht überein.'})
        else:
            login(request, user)  # Nutzer einloggen
            return redirect('home')  # Mit view-Namen auf die Homepage weiterleiten

#######################
# GEBÄUDE VERARBEITEN #
#######################
# Gebäude auslesen
@login_required
def building(request):
    building_list = Building.objects.filter(user=request.user)
    return render(request, 'emtapp/building_list.html', {'building_list': building_list})

# Neues Gebäude hinzufügen
@login_required
def building_new(request):
    submitted = False  # Variable setzten Wie genau???
    if request.method == 'POST':  # Prüfen ob es eine POST Methode ist
        form = BuildingForm(request.POST)
        if form.is_valid():  # Wenn Eingabewerte in Ordnung sind
            # new_readout = form.save(commit=False) #Eine Instanz erstellen
            # cd = form.cleaned_data #Daten in Variabel cd schreiben um beim testen auslesen können
            # assert False  # ermögliche in Django-Error-Seite page Variable cd zu betrachten
            new_building = form.save(commit=False)  # Eine Kopie des Objektes machen und nicht jetzt in DB speichern
            new_building.user = request.user  # User zum Objekt schreiben
            new_building.save()  # Objekt mit User-ID abspeichern
            return HttpResponseRedirect('/building/new?submitted=True')  # Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:
        form = BuildingForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'emtapp/building.html', {'form': form, 'submitted': submitted})

# Neuer Zähler hinzufügen
@login_required
def counter_new(request):
    submitted = False  # Variabel setzten Wie genau???
    if request.method == 'POST':  # Prüfen ob es eine POST Methode ist
        form = CounterForm(request.POST)
        if form.is_valid(): # Wenn Eingabewerte in Ordnung sind
            new_counter = form.save(commit=False)
            new_counter.user = request.user
            # new_counter.building = Building.objects.get()
            new_counter.save()
            return HttpResponseRedirect('/counter/new?submitted=True')  # Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:
        # form = modelformset_factory(Counter, fields=('name', 'building', 'counter_type', 'conversion', 'counter_overflow'), formset=CounterByUserForm)
        form = CounterForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'emtapp/counter.html', {'form': form, 'submitted': submitted})
#

# Zähler auflisten
@login_required
def counter(request):
    current_user = request.user
    user_from_db = User.objects.filter(id=current_user.id).first()
    counter_list = []
    for building in user_from_db.building_set.all():  # Alle buillding die diesem Benutzer gehören
        for counter in building.counter_set.all():    # Alle Zähler die zu diesem Building gehören
            counter_list.append(counter)
    # counter_list = Counter.objects.filter(user=request.user)  # Nur Zähler von User auflisten
    # counter_list = Counter.objects.all
    return render(request, 'emtapp/counter_list.html', {'counter_list': counter_list})

##########################
# ABLESUNGEN VERARBEITEN #
##########################
# Neue Ablesung hinzufügen
@login_required
def readout_new(request):
    submitted = False  # Variable wird 0 gesetzt
    if request.method == 'POST':  # Prüfen ob es eine POST Methode ist
        form = ReadoutForm(request.POST)  # Werte aus dem Formular aufnehmen
        if form.is_valid():  # Wenn Eingabewerte in Ordnung sind
            # Umrechnung Ablesewert in Energie muss vor schliessen des Formulars erfolgen
            new_readout = form.save(commit=False)  # Eine Instanz, Kopie, erstellen aber noch nicht speichern
            # Neue Umrechnungsmethode mit Wandlerfaktor
            z = new_readout.counter_id  # Variable um Zähler ID auszulesen
            u = Counter.objects.get(id=z).conversion  # Wandlerfaktor des Zählers auslesen
            new_readout.energy_1 = new_readout.register_1 * u  # Zählerwert in Energie umrechnen
            new_readout.energy_2 = new_readout.register_2 * u  # Zählerwert in Energie umrechnen
            new_readout.user = request.user
            form.save()
            return HttpResponseRedirect('/readout/new?submitted=True')  # Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:  # Wenn es nicht eine POST Methode ist wird dieser Teil ausgeführt
        form = ReadoutForm()  # Leeres Formular anzeigen
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'emtapp/readout.html', {'form': form, 'submitted': submitted})

# Eine bestehende Ablesung ansehen und editieren können
@login_required
def readout_edit(request, readout_pk):
    submitted = False  # Variable setzten Wie genau??
    readout = get_object_or_404(Readout, pk=readout_pk)  # Werte der Ablesung werden aus der DB gelesen
    if request.method == 'POST':  # Prüfen ob es eine POST Methode ist
        form = ReadoutForm(request.POST, instance=readout)  # Eine Instanz, Kopie, der Ablesung erstellen
        if form.is_valid():
            # Umrechnung Ablesewert in Energie muss vor schliessen des Formulars erfolgen
            new_readout = form.save(commit=False)  # Eine Instanz, Kopie, erstellen
            # Neue Umrechnungsmethode mit Wandlungsfaktor
            z = new_readout.counter_id  # Variable um Zähler ID auszulesen
            u = Counter.objects.get(id=z).conversion  # Wandlerfaktor des Zählers auslesen
            new_readout.energy_1 = new_readout.register_1 * u  # Zählerwert in Energie umrechnen
            new_readout.energy_2 = new_readout.register_2 * u  # Zählerwert in Energie umrechnen
            # cd = form.cleaned_data #Daten in Variabel cd schreiben um beim testen auslesen können
            #assert False #ermögliche in Django-Error-Seite page Variabel cd zu betrachten
            form.save()
            return HttpResponseRedirect('/readout/new?submitted=True')  # Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:
        form = ReadoutForm(instance=readout)
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'emtapp/readout_edit.html', {'form': form, 'submitted': submitted, 'readout_pk': readout_pk})

#Funktion wird ausgeführt, aber nur wenn Button-Knopf nur ausserhalb Table ist
@login_required
def readout_delete(request, readout_pk):
    readout = get_object_or_404(Readout, pk=readout_pk)  # Werte der Ablesung werden aus der DB gelesen
    readout.delete()  # Ablesung löschen
    return redirect('home')  # Liste mit Ablesungen aufrufen

#Ablesewert auflisten
@login_required
def readout_list(request, counter_pk):
    # Die Ablesewerte des angewählten Zählers anzeigen
    readout_list = Readout.objects.filter(counter_id=counter_pk).order_by('-readout_date')
    # Fehler abfangen, falls noch keine Ablesung vorgenommen wurde
    if readout_list.exists():  # Es besteht schon ein Datensatz
        return render(request, 'emtapp/readout_list.html', {'readout_list': readout_list})
    else:
        # Keine Ablesung vorhanden und somit kein Datensatz vorhanden
        return HttpResponse("<p>Es gibt noch keinen Ablesewert. Bitte zuerst Ablesung erfassen</p>")

#Diagramm darstellen
@login_required
def diagram(request, counter_pk):
    value_list = Readout.objects.filter(counter_id=counter_pk).order_by('readout_date')
    # Fehler abfangen, falls noch keine Ablesung vorgenommen wurde
    if value_list.exists():  # Es besteht schon ein Datensatz
        # first_energy_value = value_list[0].energy_1
        # last_energy_value = value_list[-1].energy_1 #Letzter Teil in Liste kann nicht direkt ausgelesen werden
        # Ein sep. Queryset, sollte verbessert werden optimale Variante liest letzte Element des Dictionary aus
        first_energy_value = Readout.objects.filter(counter_id=counter_pk).earliest('readout_date').energy_1
        last_energy_value = Readout.objects.filter(counter_id=counter_pk).latest('readout_date').energy_1
        consumption = last_energy_value-first_energy_value
        building = Building.objects.get(id=counter_pk)
        specific_consumption = consumption/building.ebf
        first_readout_date = Readout.objects.filter(counter_id=counter_pk).earliest('readout_date').readout_date
        last_readout_date = Readout.objects.filter(counter_id=counter_pk).latest('readout_date').readout_date
        period = (last_readout_date-first_readout_date).days  # Differenz in Tagen berechnen
        if 0 < period <= 245:  # Falls Ablesung länger als Heizperiode 8 Monate ist, dann keine Korrektur mehr
            consumption_heating_period = (consumption/period)*245  # Heizperiode 8 Monate
        else:
            consumption_heating_period = consumption
        return render(request, 'emtapp/diagram.html', {
            'value_list': value_list,
            'consumption': consumption,
            'building': building,
            'specific_consumption': specific_consumption,
            'period': period,
            'consumption_heating_period': consumption_heating_period
            })
    else:
        # Keine Ablesung vorhanden und somit kein Datensatz vorhanden
        return HttpResponse("<p>Es gibt noch keinen Ablesewert. Bitte zuerst Ablesung erfassen</p>")