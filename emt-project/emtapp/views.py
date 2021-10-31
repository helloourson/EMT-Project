from django.shortcuts import render
from .models import Readout, Building, Counter
from .forms import ReadoutForm, BuildingForm
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    return render(request, 'emtapp/home.html')

#View für diagramm/ erstellen
def diagramm(request):
    # ablesewerte = Zaehler.objects.all() #Alle Ojects werden ausgelesen
    # ablesewerte = Zaehler.objects.all().order_by('-zaehlerstand') #Alle Ojects auslesen und Reihenfolfe umdrechen
    # ablesewerte = Zaehler.objects.order_by('-zaehlerstand').all()[0:6] #Nur die ersten 4 Objects (Ablesungen) auslesenlle Ojects sortieren werden ausgelesen
    # values = Readout.objects.all() #Alle Werte auslesen
    id = 1 #Eine Variable definieren um nach gewünschtem Zähler zu filtern
    values = Readout.objects.filter(counter_id= id).order_by('readout_date') # Nur die Ablesewerte EerdgaszählerEG counter_id 1 anzeigen
    # Die Bezeichung des Zählers auslesen
    return render(request, 'emtapp/diagramm.html', {'values': values })

#Ablesewert auslesen
def readout(request):
    values = Readout.objects.filter(counter_id=1).order_by('readout_date') # Nur die Ablesewerte EerdgaszählerEG counter_id 1 anzeigen
    return render(request, 'emtapp/readout_list.html', {'values': values})

#Gebäude auslesen
def building(request):
    values = Building.objects.all()
    return render(request, 'emtapp/building_list.html', {'values': values})

#Zähler auslesen
def counter(request):
    values = Counter.objects.all()
    return render(request, 'emtapp/counter.html', {'values': values})

#Ablesung hinzufügen
def readout_new(request):
    submitted = False #Varable setzten Wie genau???
    if request.method == 'POST': #Prüfen ob es eine POST Methode ist
        form = ReadoutForm(request.POST)
        if form.is_valid(): #Wenn Eingabewerte in Ordnung sind
            #Umrechnung Ablesewert in Energie muss vor schliessen des Frormulars erfolgen
            newreadout = form.save(commit=False) #Eine Instanz erstellen
            #Dictionary für Umrechnung Zählerwert in Endenergie
            hs = {
                'HLM': 10,
                'HLP': 100,
                'HLD': 1000,
                'EDG': 11.452,
                'SET': 1,
                'SDT': 1
                }
            z = newreadout.counter_id #Variable um Zähler ID auszulesen
            t = Counter.objects.get(id=z).counter_type #Richtiger Zählertyp auslesen
            newreadout.energy_1 = newreadout.register_1 * hs[t] #Zählerwert in Energie umrechnen
            newreadout.energy_2 = newreadout.register_2 * hs[t] #Zählerwert in Energie umrechnen
            #cd = form.cleaned_data #Daten in Variabel cd schreiben um beim testen auslesen können
            #assert False #ermögliche in Django-Error-Seite page Varibel cd zu betrachten
            form.save()
            return HttpResponseRedirect('/readout/new?submitted=True') #Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:
        form = ReadoutForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'emtapp/readout.html', {'form': form, 'submitted': submitted})

#Gebäude hinzufügen
def building_new(request):
    submitted = False #Varable setzten Wie genau???
    if request.method == 'POST': #Prüfen ob es eine POST Methode ist
        form = BuildingForm(request.POST)
        if form.is_valid(): #Wenn Eingabewerte in Ordnung sind
            # newreadout = form.save(commit=False) #Eine Instanz erstellen
            # cd = form.cleaned_data #Daten in Variabel cd schreiben um beim testen auslesen können
            assert False #ermögliche in Django-Error-Seite page Varibel cd zu betrachten
            form.save()
            return HttpResponseRedirect('/building/new?submitted=True') #Variable submitted Wahr, die Bestätigung Eingabe war erfolgreich
    else:
        form = BuildingForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'emtapp/builiding.html', {'form': form, 'submitted': submitted})
