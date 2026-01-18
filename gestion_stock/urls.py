"""
Définition des URLs pour l'application gestion_stock
"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'gestion_stock'

urlpatterns = [
    # Page de connexion
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # Page de déconnexion
    path('logout/', views.custom_logout, name='logout'),

    # Page d'accueil de l'application (nécessite connexion)
    path('', views.index, name='index'),

    # Espaces utilisateurs
    path('espace-gerant/', views.espace_gerant, name='espace_gerant'),
    path('espace-admin/', views.espace_admin, name='espace_admin'),
    path('espace-resp-zone/', views.espace_resp_zone, name='espace_resp_zone'),
]