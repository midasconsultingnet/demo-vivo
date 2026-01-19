from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Utilisateur, Station


from django.contrib import messages

class CustomLoginView(LoginView):
    """Vue personnalisée pour la connexion"""
    template_name = 'registration/login.html'

    def form_valid(self, form):
        """Redirige vers l'espace approprié en fonction du profil de l'utilisateur"""
        user = form.get_user()

        # Ajouter un message de débogage
        print(f"Utilisateur connecté: {user.username}")
        print(f"Has utilisateur attr: {hasattr(user, 'utilisateur')}")

        # Appeler la méthode parent pour valider le formulaire et créer la session
        response = super().form_valid(form)

        if hasattr(user, 'utilisateur'):
            print(f"Profil de l'utilisateur: {user.utilisateur.profil.code}")
            if user.utilisateur.profil.code == 'GERANT_STATION':
                print("Redirection vers espace gérant")
                return HttpResponseRedirect(reverse_lazy('gestion_stock:espace_gerant'))
            elif user.utilisateur.profil.code == 'ADMIN_COMPAGNIE':
                print("Redirection vers espace admin")
                return HttpResponseRedirect(reverse_lazy('gestion_stock:espace_admin'))
            elif user.utilisateur.profil.code == 'RESPONSABLE_ZONE':
                print("Redirection vers espace responsable zone")
                return HttpResponseRedirect(reverse_lazy('gestion_stock:espace_resp_zone'))
        else:
            print("L'utilisateur n'a pas d'objet utilisateur associé")

        # Par défaut, rediriger vers la page d'accueil
        print("Redirection vers la page d'accueil")
        return HttpResponseRedirect(reverse_lazy('gestion_stock:index'))


@login_required
def index(request):
    """
    Vue de la page d'accueil de l'application de gestion de stock
    Nécessite d'être connecté pour y accéder
    """
    # Ajouter un message de débogage
    print(f"Page d'accueil visitée par: {request.user.username}")
    print(f"Has utilisateur attr: {hasattr(request.user, 'utilisateur')}")

    # Vérifier si l'utilisateur a un profil associé
    if hasattr(request.user, 'utilisateur'):
        print(f"Profil de l'utilisateur: {request.user.utilisateur.profil.code}")
        # Rediriger vers l'espace approprié en fonction du profil
        if request.user.utilisateur.profil.code == 'GERANT_STATION':
            print("Redirection vers espace gérant depuis index")
            return redirect('gestion_stock:espace_gerant')
        elif request.user.utilisateur.profil.code == 'ADMIN_COMPAGNIE':
            print("Redirection vers espace admin depuis index")
            return redirect('gestion_stock:espace_admin')
        elif request.user.utilisateur.profil.code == 'RESPONSABLE_ZONE':
            print("Redirection vers espace responsable zone depuis index")
            return redirect('gestion_stock:espace_resp_zone')

    return render(request, 'index.html')


@login_required
def espace_gerant(request):
    """
    Espace du gérant de station
    """
    # Ajouter un message de débogage
    print(f"Espace gérant visité par: {request.user.username}")
    print(f"Has utilisateur attr: {hasattr(request.user, 'utilisateur')}")

    # Charger explicitement l'utilisateur personnalisé
    try:
        utilisateur_personnalise = request.user.utilisateur
        print(f"Profil trouvé: {utilisateur_personnalise.profil.code}")

        if utilisateur_personnalise.profil.code != 'GERANT_STATION':
            print("Profil incorrect pour l'espace gérant")
            return HttpResponseForbidden("Accès non autorisé - Profil incorrect")

        print("Accès autorisé à l'espace gérant")

        # Récupérer les stations gérées par ce gérant
        stations = utilisateur_personnalise.stations_gerees.all()

        context = {
            'stations': stations,
            'titre_espace': 'Espace Gérant de Station'
        }
        return render(request, 'espace_gerant.html', context)
    except Utilisateur.DoesNotExist:
        print("Utilisateur sans profil trouvé")
        return HttpResponseForbidden("Accès non autorisé - Utilisateur sans profil")


@login_required
def espace_admin(request):
    """
    Espace de l'administrateur compagnie
    """
    # Charger explicitement l'utilisateur personnalisé
    try:
        utilisateur_personnalise = request.user.utilisateur
        if utilisateur_personnalise.profil.code != 'ADMIN_COMPAGNIE':
            return HttpResponseForbidden("Accès non autorisé - Profil incorrect")

        # Récupérer toutes les stations de la compagnie
        # Pour simplifier, on suppose que l'admin voit toutes les stations
        stations = Station.objects.all()

        context = {
            'stations': stations,
            'titre_espace': 'Espace Administrateur Compagnie'
        }
        return render(request, 'espace_admin.html', context)
    except Utilisateur.DoesNotExist:
        return HttpResponseForbidden("Accès non autorisé - Utilisateur sans profil")


@login_required
def espace_resp_zone(request):
    """
    Espace du responsable zone
    """
    # Charger explicitement l'utilisateur personnalisé
    try:
        utilisateur_personnalise = request.user.utilisateur
        if utilisateur_personnalise.profil.code != 'RESPONSABLE_ZONE':
            return HttpResponseForbidden("Accès non autorisé - Profil incorrect")

        # Récupérer les stations supervisées par ce responsable de zone
        stations = utilisateur_personnalise.stations_supervisees.all()

        context = {
            'stations': stations,
            'titre_espace': 'Espace Responsable Zone'
        }
        return render(request, 'espace_resp_zone.html', context)
    except Utilisateur.DoesNotExist:
        return HttpResponseForbidden("Accès non autorisé - Utilisateur sans profil")


def custom_logout(request):
    """
    Vue personnalisée pour la déconnexion
    """
    logout(request)
    return redirect('gestion_stock:login')

def health_check(request):
    return JsonResponse({'status': 'ok', 'healthy': True})