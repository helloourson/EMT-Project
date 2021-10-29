from django.shortcuts import render
from .models import Readout

# Create your views here.
def home(request):
    return render(request, 'emtapp/home.html')


#View für diagramm/ erstellen
def diagramm(request):
    # ablesewerte = Zaehler.objects.all() #Alle Ojects werden ausgelesen
    # ablesewerte = Zaehler.objects.all().order_by('-zaehlerstand') #Alle Ojects auslesen und Reihenfolfe umdrechen
    # ablesewerte = Zaehler.objects.order_by('-zaehlerstand').all()[0:6] #Nur die ersten 4 Objects (Ablesungen) auslesenlle Ojects sortieren werden ausgelesen
    values = Readout.objects.filter(counter_id=1).order_by('readout_date') # Nur die Ablesewerte EerdgaszählerEG counter_id 1 anzeigen
    # Die Bezeichung des Zählers auslesen
    return render(request, 'emtapp/diagramm.html', {'values': values })

#Ablesewert aulisten
def readout(request):
    values = Readout.objects.filter(counter_id=1).order_by('readout_date') # Nur die Ablesewerte EerdgaszählerEG counter_id 1 anzeigen
    return render(request, 'emtapp/readout.html', {'values': values})
