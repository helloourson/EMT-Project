from django.contrib import admin
from .models import Counter, Readout, Building #Model Counter, Readout, Building importieren

# Register your models here.
class CounterAdmin(admin.ModelAdmin):
    #In /admin/emtapp/counter/ sollen die Eigenschaften name, counter_type, counter_overflow angezeigt werden
    list_display = ('name', 'counter_type', 'counter_overflow')
    ordering = ('name',)     #Die Einträge sollen nach name aufgelistet werden

admin.site.register(Counter, CounterAdmin)

class ReadoutAdmin(admin.ModelAdmin):
    #In /admin/emtapp/ReadoutAdmi/ sollen die Eigenschaften name, counter_type, counter_overflow angezeigt werden
    list_display = ('counter', 'readout_date', 'register_1','energy_1', 'register_2', 'energy_2', 'comment')
    #Die Einträge sollen counter und readout_date aufgelistet werden
    ordering = ('counter', 'readout_date', )

admin.site.register(Readout, ReadoutAdmin)

class BuildingAdmin(admin.ModelAdmin):
    #In /admin/emtapp/BuildingAdmin/ sollen die Eigenschaften angezeigt werden
    list_display = ('street_number', 'city', 'building_type','year_construction', 'ebf', 'tenant', 'heating_type', 'distribution_type', 'hotwater_type', 'comment')
    ordering = ('city',)

admin.site.register(Building, BuildingAdmin)
