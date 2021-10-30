from django import forms
from django.forms import ModelForm
from .models import Readout

#Readout Form Energiewerte auslesen und darstellen
class ReadoutForm(ModelForm):
    class Meta:
        model = Readout
        #fields = '__all__'
        fields = ['counter','readout_date', 'register_1', 'register_2', 'comment']
