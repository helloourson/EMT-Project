from django import forms
from django.forms import ModelForm
from .models import Readout, Building, Counter
from django.forms import BaseModelFormSet

# # Formular um Energiewerte zu erfassen
# class ReadoutForm(ModelForm):
#     class Meta:
#         model = Readout
#         #fields = '__all__'
#         fields = ['counter', 'readout_date', 'register_1', 'register_2', 'comment']
# # --> Verbesserung nur Zähler des eingeloggten Nutzers anzeigen

# Formular um Energiewerte zu erfassen
class ReadoutForm(ModelForm):
    # Vorgehen um im Formular nur die Zähler des eingeloggten Nutzers anzuzeigen
    def __init__(self, user=None, form=None, *args, **kwargs):
        self.user = user
        super(ReadoutForm, self).__init__(form, *args, **kwargs)  # Rufe Konstruktor der ModelForm auf
        # if self.user:  # Wenn ein user eingeloggt ist
            ### Code ist falsch hier sollte auf die buildings des eingeloggten users verwiesent werden
            # self.fields['counter'].queryset = Counter.objects.filter(user_id=self.user.id)  # Filter counter auf user mitgegeben

        ### Funktioniert, dass ich ein Zähler eines Gebäudes anzeigen kann
        # self.fields['counter'].queryset = Counter.objects.filter(building_id=8)
        ### Wie mache ich es, dass nur die Zähler des eingeloggten users z.B. A angezeigt wird?
    class Meta:
        model = Readout
        # fields = '__all__'
        fields = ['counter', 'readout_date', 'register_1', 'register_2', 'comment']

# Formular um Gebäude erfassen
class BuildingForm(ModelForm):
    class Meta:
        model = Building
        # fields = '__all__'
        fields = ['street_number', 'city', 'building_type', 'year_construction',
                  'ebf', 'tenant', 'heating_type', 'distribution_type',
                  'hotwater_type', 'comment']

#  class CounterFormFilter(forms.Form):
#      model_choice = forms.ModelChoiceField(queryset= Building.objects.filter(user_id=3), initial=0)

# Formular um Zähler zufassen
class CounterForm(ModelForm):
    # Vorgehen um im Formular nur die Gebäude des eingeloggten Nutzers anzuzeigen
    def __init__(self, user=None, form=None, *args, **kwargs):
        self.user = user
        super(CounterForm, self).__init__(form, *args, **kwargs)  # Rufe Konstruktor der ModelForm auf
        if self.user:  # Wenn ein user eingeloggt ist
            self.fields['building'].queryset = Building.objects.filter(user_id=self.user.id)  # Filter building auf mitgegeben user

    class Meta:
        model = Counter
        # fields = '__all__'
        fields = ['building', 'counter_type', 'name', 'conversion', 'counter_overflow']

# class CounterForm(forms.Form):
#     model_choice = forms.ModelChoiceField(queryset= Building.objects.filter(user_id=3), initial=0)

# class CounterByUserForm(BaseModelFormSet):
#     def __init__(self, current_user, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.queryset = Building.objects.filter(user_id=current_user)