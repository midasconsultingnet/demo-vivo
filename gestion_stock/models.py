from django.db import models


class Profil(models.Model):
    code = models.CharField(max_length=50, unique=True)
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle


class CompagniePetrolier(models.Model):
    nom = models.CharField(max_length=150)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class MarqueCompagnie(models.Model):
    nom = models.CharField(max_length=150)
    compagnie_petrolier = models.ForeignKey(CompagniePetrolier, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


from django.contrib.auth.models import User

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    login = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=255)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom and self.nom else self.login

    @property
    def stations_gerees(self):
        """Retourne les stations gérées par cet utilisateur"""
        return Station.objects.filter(gerant=self)


class Station(models.Model):
    nom = models.CharField(max_length=150)
    informations = models.JSONField(null=True, blank=True)

    compagnie_petrolier = models.ForeignKey(CompagniePetrolier, on_delete=models.CASCADE)
    marque = models.ForeignKey(MarqueCompagnie, on_delete=models.CASCADE)
    gerant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        help_text="Un gérant peut gérer une ou plusieurs stations",
        related_name='stations_gerees'
    )  # gérant de la station

    responsable_zone = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Responsable de zone pour cette station",
        related_name='stations_supervisees'
    )

    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Station"
        verbose_name_plural = "Stations"


class Produit(models.Model):
    TYPE_CHOICES = [
        ('CARBURANT', 'Carburant'),
        ('LUBRIFIANT', 'Lubrifiant'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    libelle = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.libelle


class Cuve(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    capacite = models.DecimalField(max_digits=15, decimal_places=3)
    barremage = models.JSONField()  # Champ obligatoire
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"Cuve {self.id} - {self.station.nom}"


class Pistolet(models.Model):
    code = models.CharField(max_length=50, blank=True)
    cuve = models.ForeignKey(Cuve, on_delete=models.CASCADE)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"Pistolet {self.code}" if self.code else f"Pistolet {self.id}"


class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('ACHAT', 'Achat'),
        ('VENTE', 'Vente'),
        ('INVENTAIRE', 'Inventaire'),
    ]
    
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    cuve = models.ForeignKey(Cuve, on_delete=models.SET_NULL, null=True, blank=True)

    type_mouvement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantite = models.DecimalField(max_digits=15, decimal_places=3)
    date_mouvement = models.DateTimeField()

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    infos = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.libelle} - {self.quantite}"


class StockStation(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('station', 'produit')

    def __str__(self):
        return f"Stock {self.station.nom} - {self.produit.libelle}: {self.quantite}"