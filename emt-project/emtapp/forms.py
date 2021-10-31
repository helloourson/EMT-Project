from django import forms
from django.forms import ModelForm
from .models import Readout, Building

#Formular um Energiewerte zu erfassen, umrechnen und in DB schreiben
class ReadoutForm(ModelForm):
    class Meta:
        model = Readout
        #fields = '__all__'
        fields = ['counter','readout_date', 'register_1', 'register_2', 'comment']

#Formular um Gebäude zuerfassen
class BuildingForm(ModelForm):
    class Meta:
        model = Building
        fields = '__all__'
