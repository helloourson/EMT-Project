#urls.py erstellen in Emtapp
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authentifizierung
    path('signup/', views.signup_user, name='signup_user'),  # Anmelden
    path('logout/', views.logout_user, name='logout_user'),  # Ausloggen
    path('login/', views.login_user, name='login_user'),  # Einloggen

    # Gebäude
    path('building/', views.building, name='building'),
    path('building/new', views.building_new, name='building_new'),

    # Zähler
    path('counter/', views.counter, name='counter'),
    path('counter/new', views.counter_new, name='counter_new'),

    # Ablesungen
    path('readout/new', views.readout_new, name='readout_new'),
    path('readout/<int:readout_pk>/edit', views.readout_edit, name='readout_edit'),
    path('readout/<int:readout_pk>/delete', views.readout_delete, name='readout_delete'),

    # Datenvisualisierung
    path('readout/<int:counter_pk>', views.readout_list, name='readout_list'),
    path('diagram/<int:counter_pk>', views.diagram, name='diagram'),
]
