from django.shortcuts import render
from .models import Readout, Building, Counter
from .forms import ReadoutForm, BuildingForm, CounterForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect


# Create your views here.
def home(request):
    return render(request, 'emtapp/home.html')

#Gebäude auslesen
def building(request):
    values = Building.objects.all()
    return render(request, 'emtapp/building_list.html', {'values': values})

#Neues Gebäude hinzufügen
def building_new(request):
    submitted = False #Varable setzten Wie genau???
    if request.method == 'POST': #Prüfen ob es eine POST Methode ist
        form = BuildingForm(request.POST)
        if form.is_valid(): #Wenn Eingabewerte in Ordnung sind
            # newreadout = form.save(commit=False) #Eine Instanz erstellen
            # cd = form.cleaned_data #Daten in Variabel cd schreiben um beim testen auslesen können
            # assert False #ermögliche in Django-Error-Seite page Varibel cd zu betrachten
            form.save()
            return HttpResponseRedirect('/building/new?submitted=True') #Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:
        form = BuildingForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'emtapp/builiding.html', {'form': form, 'submitted': submitted})

#Neuer Zähler hinzufügen
def counter_new(request):
    submitted = False #Variabel setzten Wie genau???
    if request.method == 'POST': #Prüfen ob es eine POST Methode ist
        form = CounterForm(request.POST)
        if form.is_valid(): #Wenn Eingabewerte in Ordnung sind
            form.save()
            return HttpResponseRedirect('/counter/new?submitted=True') #Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:
        form = CounterForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'emtapp/counter.html', {'form': form, 'submitted': submitted})
#

#Zähler auflisten
def counter(request):
    counter_list = Counter.objects.all()
    return render(request, 'emtapp/counter_list.html', {'counter_list': counter_list})

#Neue Ablesung hinzufügen
def readout_new(request):
    submitted = False #Varable setzten Wie genau???
    if request.method == 'POST': #Prüfen ob es eine POST Methode ist
        form = ReadoutForm(request.POST) #Werte aus dem Formular aufnehmen
        if form.is_valid(): #Wenn Eingabewerte in Ordnung sind
            #Umrechnung Ablesewert in Energie muss vor schliessen des Formulars erfolgen
            newreadout = form.save(commit=False) #Eine Instanz, Kopie, erstellen
            #Neue Umrechnungsmethode mit Wandlungsfaktor
            z = newreadout.counter_id #Variable um Zähler ID auszulesen
            u = Counter.objects.get(id=z).conversion #Wandlerfaktor des Zählers auslesen
            newreadout.energy_1 = newreadout.register_1 * u #Zählerwert in Energie umrechnen
            newreadout.energy_2 = newreadout.register_2 * u #Zählerwert in Energie umrechnen
            form.save()
            return HttpResponseRedirect('/readout/new?submitted=True') #Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else: #Wenn es nicht eine POST Methode ist wird dieser Teil ausgeführt
        form = ReadoutForm() #Leeres Formular anzeigen
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'emtapp/readout.html', {'form': form, 'submitted': submitted})

#Eine bestehende Ablesung ansehen und editieren können
def readout_edit(request, readout_pk):
    submitted = False #Varable setzten Wie genau??
    readout = get_object_or_404(Readout, pk=readout_pk) #Werte der Ablesung werden aus der DB gelesen
    if request.method == 'POST': #Prüfen ob es eine POST Methode ist
        form = ReadoutForm(request.POST, instance=readout) #Eine Instanz, Kopie, der Ablesung erstellen
        if form.is_valid():
            #Umrechnung Ablesewert in Energie muss vor schliessen des Frormulars erfolgen
            newreadout = form.save(commit=False) #Eine Instanz, Kopie, erstellen
            #Neue Umrechnungsmethode mit Wandlungsfaktor
            z = newreadout.counter_id #Variable um Zähler ID auszulesen
            u = Counter.objects.get(id=z).conversion #Wandlerfaktor des Zählers auslesen
            newreadout.energy_1 = newreadout.register_1 * u #Zählerwert in Energie umrechnen
            newreadout.energy_2 = newreadout.register_2 * u #Zählerwert in Energie umrechnen
            # cd = form.cleaned_data #Daten in Variabel cd schreiben um beim testen auslesen können
            #assert False #ermögliche in Django-Error-Seite page Varibel cd zu betrachten
            form.save()
            return HttpResponseRedirect('/readout/new?submitted=True') #Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:
        form = ReadoutForm(instance=readout)
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'emtapp/readout.html', {'form': form, 'submitted': submitted, 'readout_pk': readout_pk})

#FUNKTIONIERT NICHT WAAAAARUM? ZUSAMMENHANG MIT POST???????????????
# #Ablesung löschen
# def readout_delete(request, readout_pk):
#     readout = get_object_or_404(Readout, pk=readout_pk) #Werte der Ablesung werden aus der DB gelesen
#     if request.method == 'POST': #Prüfen ob es eine POST Methode ist
#         readout.delete() #Ablesung löschen
#         return HttpResponseRedirect('home') #Zurück zur Ableseliste
#     return render(request, 'emtapp/readout_list.html')

#ALTERNATIVER VERSUCH Ablesung löschen
#FUNKTIONIERT NUR WENN URL EINGEGEBEN WIRD NICHT MIT BUTTON !!!!!!!!
def readout_delete(request, readout_pk):
    readout = get_object_or_404(Readout, pk=readout_pk) #Werte der Ablesung werden aus der DB gelesen
    readout.delete() #Ablesung löschen
    return redirect('home') #Liste mit Ablesungen aufrufen
###########################################################################

#Ablesewert auflisten
def readout(request, counter_pk):
    # Die Ablesewerte des angewählten Zählers anzeigen
    readout_list = Readout.objects.filter(counter_id=counter_pk).order_by('-readout_date')
    # name_list = {"Fido": 8 , "Sally":17, "Sean": 10}
    return render(request, 'emtapp/readout_list.html', {'readout_list': readout_list})

#Diagramm darstellen
def diagramm(request, counter_pk):
    value_list = Readout.objects.filter(counter_id= counter_pk).order_by('readout_date')
    # first_energy_value = value_list[0].energy_1
    # last_energy_value = value_list[-1].energy_1
    first_energy_value = Readout.objects.filter(counter_id= counter_pk).earliest('readout_date').energy_1
    last_energy_value = Readout.objects.filter(counter_id= counter_pk).latest('readout_date').energy_1
    consumption = last_energy_value-first_energy_value
    building = Building.objects.get(id=counter_pk)
    specific_consumption = consumption/building.ebf

    first_readout_date = Readout.objects.filter(counter_id= counter_pk).earliest('readout_date').readout_date
    last_readout_date = Readout.objects.filter(counter_id= counter_pk).latest('readout_date').readout_date
    dauer = (last_readout_date-first_readout_date).days #Differenz in Tagen berechnen
    consumption_heating_period = (consumption/dauer)*245 #Heizperiode 8 Monate

    return render(request, 'emtapp/diagramm.html', {
        'value_list': value_list,
        'consumption': consumption,
        'building':building,
        'specific_consumption':specific_consumption,
        'dauer':dauer,
        'consumption_heating_period': consumption_heating_period
        })
