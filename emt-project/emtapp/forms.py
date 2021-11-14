from django import forms
from django.forms import ModelForm
from .models import Readout, Building, Counter

#Formular um Energiewerte zu erfassen, umrechnen und in DB schreiben
class ReadoutForm(ModelForm):
    class Meta:
        model = Readout
        #fields = '__all__'
        fields = ['counter', 'readout_date', 'register_1', 'register_2', 'comment']

#Formular um Gebäude erfassen
class BuildingForm(ModelForm):
    class Meta:
        model = Building
        fields = '__all__'

#Formular um Gebäude zufassen
class CounterForm(ModelForm):
    class Meta:
        model = Counter
        fields = '__all__'
