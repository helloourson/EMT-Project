from django import forms
from django.forms import ModelForm
from .models import Readout, Building, Counter

# Formular um Energiewerte zu erfassen
class ReadoutForm(ModelForm):
    class Meta:
        model = Readout
        #fields = '__all__'
        fields = ['counter', 'readout_date', 'register_1', 'register_2', 'comment']

# Formular um Gebäude erfassen
class BuildingForm(ModelForm):
    class Meta:
        model = Building
        # fields = '__all__'
        fields = ['street_number', 'city', 'building_type', 'year_construction',
                  'ebf', 'tenant', 'heating_type', 'distribution_type', 'comment']

# Formular um Zähler zufassen
class CounterForm(ModelForm):
    class Meta:
        model = Counter
        # fields = '__all__'
        fields = ['name', 'building', 'counter_type', 'conversion', 'counter_overflow']
        # fields = ['building']

# class CounterForm(forms.Form):
#     model_choice = forms.ModelChoiceField(queryset= Building.objects.filter(user_id=3), initial=0)