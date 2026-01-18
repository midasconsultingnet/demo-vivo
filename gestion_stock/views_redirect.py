from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def redirect_to_login(request):
    """
    Redirige vers la page de connexion si l'utilisateur n'est pas connecté,
    sinon vers la page d'accueil de l'application
    """
    if request.user.is_authenticated:
        # Si l'utilisateur est connecté, rediriger vers l'espace approprié
        if hasattr(request.user, 'utilisateur'):
            if request.user.utilisateur.profil.code == 'GERANT_STATION':
                return redirect('gestion_stock:espace_gerant')
            elif request.user.utilisateur.profil.code == 'ADMIN_COMPAGNIE':
                return redirect('gestion_stock:espace_admin')
            elif request.user.utilisateur.profil.code == 'RESPONSABLE_ZONE':
                return redirect('gestion_stock:espace_resp_zone')

        # Par défaut, rediriger vers la page d'accueil
        return redirect('gestion_stock:index')
    else:
        return redirect('gestion_stock:login')