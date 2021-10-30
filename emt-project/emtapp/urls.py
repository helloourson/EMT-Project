#urls.py erstellen in Emtapp

from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('readout/', views.readout, name='readout'),
    path('building/', views.building, name='building'),
    path('counter/', views.counter, name='counter'),
    path('diagramm/', views.diagramm, name='diagramm'),
    path('add_readout/', views.add_readout, name='add_readout'),
]
