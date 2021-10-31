#urls.py erstellen in Emtapp
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('readout/', views.readout, name='readout'),
    path('building/', views.building, name='building'),
    path('counter/', views.counter, name='counter'),
    path('diagramm/', views.diagramm, name='diagramm'),
    path('building/new', views.building_new, name='building_new'),
    path('readout/new', views.readout_new, name='readout_new'),

]
