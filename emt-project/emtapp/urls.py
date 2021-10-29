#urls.py erstellen in Emtapp

from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('readout/', views.readout, name='readout'),
    path('diagramm/', views.diagramm, name='diagramm'),
]
