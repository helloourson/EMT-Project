from django import forms
from django.forms import ModelForm
from .models import Readout, Building, Counter
from django.forms import BaseModelFormSet

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



#  class CounterFormFilter(forms.Form):
#      model_choice = forms.ModelChoiceField(queryset= Building.objects.filter(user_id=3), initial=0)

# Formular um Zähler zufassen
class CounterForm(ModelForm):
    model_choice = forms.ModelChoiceField(queryset= Building.objects.filter(user_id=3), initial=0)
    class Meta:
        model = Counter
        # fields = '__all__'
        fields = ['name', 'model_choice', 'counter_type', 'conversion', 'counter_overflow']
        # fields = ['building']

# class CounterForm(forms.Form):
#     model_choice = forms.ModelChoiceField(queryset= Building.objects.filter(user_id=3), initial=0)


class CounterByUserForm(BaseModelFormSet):
    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Building.objects.filter(user_id=current_user)