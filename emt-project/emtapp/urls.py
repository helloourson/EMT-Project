#urls.py erstellen in Emtapp
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('building/', views.building, name='building'),
    path('building/new', views.building_new, name='building_new'),

    path('counter/', views.counter, name='counter'),
    path('counter/new', views.counter_new, name='counter_new'),

    path('readout/new', views.readout_new, name='readout_new'),
    path('readout/<int:counter_pk>', views.readout, name='readout'),
    path('readout/<int:readout_pk>/edit', views.readout_edit, name='readout_edit'),
    path('readout/<int:readout_pk>/delete', views.readout_delete, name='readout_delete'),

    path('diagramm/<int:counter_pk>', views.diagramm, name='diagramm'),
]
