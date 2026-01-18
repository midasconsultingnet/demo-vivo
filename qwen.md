# Système de gestion de stock – Station-service

---

## 1. Contexte métier

Ce projet vise à créer un **système simplifié de gestion de stock** pour une station-service, permettant aux gérants de station et aux administrateurs de compagnies pétrolières de suivre de manière fiable les flux de carburants et de lubrifiants, avec traçabilité complète des opérations.

### Objectifs principaux
1. Gestion des utilisateurs et rôles :
   - Gérant de station
   - Administrateur compagnie pétrolière
   - Responsable de zone
2. Gestion des compagnies pétrolières et marques.
3. Gestion des stations avec leur gérant, cuves et pistolets.
4. Gestion des produits : carburants (SP, PL, Gasoil) et lubrifiants.
5. Gestion des mouvements de stock :
   - ACHAT
   - VENTE
   - INVENTAIRE
6. Calcul automatique :
   - Stock théorique = somme des achats − somme des ventes
   - Stock réel = dernier inventaire physique
   - Écart = stock réel − stock théorique
7. Traçabilité via un champ JSON `infos` dans chaque mouvement, incluant : numéro facture, BL, pistolet, compteur, observations, etc.

### Règles métier clés
- Un gérant peut gérer une ou plusieurs stations.
- Chaque station a un seul gérant.
- Les utilisateurs ont accès uniquement aux données correspondant à leur profil.
- Les mouvements sont historisés et **immuables**.
- Les écarts de stock sont constatés mais ne modifient jamais les anciens mouvements.

---

## 2. Contexte technique

### Technologie principale
- **Django (Python)** : framework web monolithique pour gérer :
  - Logique métier
  - Interface utilisateur (templates HTML/CSS/JS)
  - Authentification et rôles
  - Migrations et base de données

### Base de données
- **PostgreSQL** pour sa robustesse et support natif du JSON.
- Les Models Django seront synchronisés avec PostgreSQL.
- Champ `infos JSON` pour stocker les données complémentaires des mouvements (achat, vente, inventaire).

---

## 3. Architecture simplifiée

[Navigateur web]
|
v
[Application Django]
- Views : logique métier et calcul stock
- Templates : interface HTML
- Models : interaction avec PostgreSQL
|
v
[Base PostgreSQL]

- Pas d’API REST : toutes les opérations et l’affichage sont côté serveur.
- Les calculs de stock théorique, réel et écart se font dans Django à partir des mouvements.
- Les fichiers statiques et médias (images, documents) sont servis par Django ou Nginx en production.

---

## 4. Modèles de données PostgreSQL / Django

### Compagnie pétrolière

```python
class CompagniePetrolier(models.Model):
    nom = models.CharField(max_length=150)
    actif = models.BooleanField(default=True)

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    login = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=255)
    profil = models.CharField(max_length=50)  # GERANT_STATION / ADMIN / RESPONSABLE_ZONE

class Station(models.Model):
    nom = models.CharField(max_length=150)
    informations = models.JSONField(null=True)
    compagnie = models.ForeignKey(CompagniePetrolier, on_delete=models.CASCADE)
    gérant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

class Produit(models.Model):
    code = models.CharField(max_length=50)
    libelle = models.CharField(max_length=100)
    type = models.CharField(max_length=20)  # SP, PL, Gasoil, Lubrifiant

class Cuve(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    capacité = models.DecimalField(max_digits=15, decimal_places=3)
    barremage = models.JSONField(null=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

class Pistolet(models.Model):
    cuve = models.ForeignKey(Cuve, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

class MouvementStock(models.Model):
    ACHAT = 'ACHAT'
    VENTE = 'VENTE'
    INVENTAIRE = 'INVENTAIRE'
    TYPE_CHOICES = [(ACHAT, 'Achat'), (VENTE, 'Vente'), (INVENTAIRE, 'Inventaire')]

    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    cuve_id = models.IntegerField(null=True)
    type_mouvement = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantite = models.DecimalField(max_digits=15, decimal_places=3)
    date_mouvement = models.DateTimeField()
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    infos = models.JSONField(null=True)  # données complémentaires (facture, BL, pistolet, etc.)
5. Workflow des mouvements de stock
| Type de mouvement | Description                        | Champ `infos` JSON                                            |
| ----------------- | ---------------------------------- | ------------------------------------------------------------- |
| ACHAT             | Entrée de stock depuis fournisseur | numéro_facture, date_facture, BL, transporteur, volume        |
| VENTE             | Sortie de stock via pistolet       | pistolet_id, index_debut, index_fin, ticket_vente, mode_vente |
| INVENTAIRE        | Constat physique du stock          | méthode, niveau_mesure, température, observations             |

Calculs

Stock théorique = somme des achats − somme des ventes
Stock réel = dernier inventaire enregistré
Écart = stock réel − stock théorique

6. Sécurité et rôles

Gérant : accès à sa station uniquement
Administrateur : accès à toutes les stations de la compagnie
Responsable zone : accès aux stations de sa zone
Les mouvements sont immuables : toute correction passe par un nouveau mouvement
Authentification et gestion des rôles via Django

7. Objectif final

Fournir une application web robuste, simple et sécurisée, permettant :
La gestion quotidienne de stock par le gérant de station
La supervision par l’administrateur de compagnie
Une traçabilité complète grâce aux mouvements historisés et au champ JSON infos
Une solution évolutive pour intégrer ultérieurement reporting, alertes et automatisation
