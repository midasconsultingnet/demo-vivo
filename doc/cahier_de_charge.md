# 📘 CAHIER DES CHARGES  
## Système de gestion de stock – Station-service

---

## 1. CONTEXTE ET OBJECTIF

Les stations-service doivent assurer un suivi rigoureux des stocks de carburants et produits associés afin de :
- maîtriser les entrées (achats),
- contrôler les sorties (ventes),
- détecter les pertes ou écarts,
- assurer la traçabilité des opérations.

Ce projet vise à mettre en place un **système informatique simplifié** permettant la **gestion des stocks** dans une station-service, avec une **vision centralisée pour les compagnies pétrolières**.

---

## 2. OBJECTIFS DU SYSTÈME

- Gérer les utilisateurs et leurs rôles
- Gérer les compagnies pétrolières et leurs stations
- Gérer les produits (carburants, lubrifiants)
- Gérer les cuves et pistolets
- Enregistrer les mouvements de stock (achat, vente, inventaire)
- Calculer automatiquement :
  - le stock théorique
  - le stock réel
  - les écarts de stock
- Assurer la traçabilité et l’historique des opérations

---

## 3. PÉRIMÈTRE FONCTIONNEL

### Inclus
- Gestion de stock
- Gestion des utilisateurs
- Suivi par station
- Historique des mouvements
---

## 4. ACTEURS DU SYSTÈME

### 4.1 Profils utilisateurs

| Profil | Description |
|------|------------|
| Gérant de station | Gère les opérations quotidiennes d’une station |
| Administrateur compagnie | Supervise toutes les stations d’une compagnie |
| Responsable zone | Supervise un groupe de stations |

---

## 5. GESTION DES UTILISATEURS

### Fonctionnalités
- Authentification par login / mot de passe
- Activation / désactivation de compte
- Attribution d’un profil

### Règles métier
- Un utilisateur possède **un seul profil**
- Un gérant est affecté à **une seule ou plusieurs stations**
- Une station possède **un seul gérant**

---

## 6. STRUCTURE ORGANISATIONNELLE

### 6.1 Compagnie pétrolière
- Une compagnie peut gérer plusieurs stations
- Une compagnie peut avoir plusieurs marques

### 6.2 Station-service
- Une station appartient à une compagnie
- Une station est rattachée à une marque
- Une station possède :
  - un gérant
  - des cuves
  - des pistolets

---

## 7. GESTION DES PRODUITS

### Types de produits
- Carburants :
  - SP
  - Gasoil
  - Pétrole
- Lubrifiants

### Règles
- Un produit est unique
- Un produit peut être stocké dans plusieurs stations
- Une cuve contient **un seul produit**

---

## 8. GESTION DES CUVE ET PISTOLETS

### Cuve
- Appartient à une station
- Contient un seul produit
- Possède :
  - une capacité
  - un barémage (JSON)

### Pistolet
- Appartient à une cuve
- Sert à la distribution du carburant

---

## 9. GESTION DE STOCK

### 9.1 Principe fondamental

Le stock n’est **jamais saisi directement**.  
Il est **calculé à partir des mouvements**.

---

### 9.2 Types de mouvements

| Type | Description |
|----|------------|
| ACHAT | Entrée de stock |
| VENTE | Sortie de stock |
| INVENTAIRE | Constat du stock réel |

---

### 9.3 Stock théorique

**Définition**  
Quantité calculée à partir des mouvements :

Stock théorique = Somme des ACHATS – Somme des VENTES

📌 Le stock théorique reflète ce que le système “pense” qu’il reste.

---

### 9.4 Stock réel

**Définition**  
Quantité réellement mesurée dans la cuve lors d’un inventaire physique.

📌 Le stock réel est enregistré via un mouvement de type `INVENTAIRE`.

Chaque mouvement de stock contient, en plus des informations de base,
un champ `infos` au format JSON permettant de stocker les données
complémentaires spécifiques au type de mouvement (achat, vente,
inventaire).

### Informations complémentaires des mouvements

Chaque mouvement de stock peut contenir un ensemble d’informations
complémentaires stockées dans un champ structuré de type JSON.

Ce champ permet de conserver des données variables sans alourdir
le modèle de données ni créer de nouvelles tables.

#### Mouvements d’achat (ACHAT)

Les informations complémentaires peuvent inclure :
- numéro de facture
- date de facture
- fournisseur
- numéro de bon de livraison
- volume livré
- transporteur

Ces informations permettent d’assurer la traçabilité des livraisons
et le contrôle des entrées de stock.

#### Mouvements de vente (VENTE)

Les informations complémentaires peuvent inclure :
- pistolet utilisé
- index compteur début / fin
- numéro de ticket de vente
- mode de vente

Ces données permettent le rapprochement entre les ventes physiques
et les sorties de stock.

#### Mouvements d’inventaire (INVENTAIRE)

Les informations complémentaires peuvent inclure :
- méthode de mesure (barémage, jauge, estimation)
- niveau mesuré
- conditions de mesure
- observations

Ces informations assurent la traçabilité et la fiabilité des inventaires.

---

### 9.5 Écart de stock

**Formule**
Écart = Stock réel – Stock théorique

| Résultat | Interprétation |
|-------|----------------|
| Écart = 0 | Stock conforme |
| Écart < 0 | Perte / fuite / erreur |
| Écart > 0 | Surplus |

---

## 10. INVENTAIRE

### Principe
- L’inventaire est un **constat**
- Il ne modifie pas les anciens mouvements
- Il permet de détecter les écarts

### Règles
- Chaque inventaire crée un mouvement `INVENTAIRE`
- Le dernier inventaire représente le stock réel actuel
- Les écarts sont visibles mais non corrigés automatiquement

---

## 11. TRAÇABILITÉ ET HISTORIQUE

Chaque mouvement de stock doit contenir :
- la station
- le produit
- la cuve (si applicable)
- le type de mouvement
- la quantité
- la date
- l’utilisateur responsable

Chaque mouvement de stock est historisé de manière immuable.
Les informations associées au mouvement incluent :
- les données quantitatives (quantité, date, type),
- les informations contextuelles stockées au format JSON,
- l’utilisateur ayant effectué l’opération.

Les mouvements ne peuvent pas être modifiés ou supprimés après validation.
Toute correction doit faire l’objet d’un nouveau mouvement.

---

## 12. SÉCURITÉ ET CONTRÔLES

### Accès aux données
- Le gérant voit uniquement sa station
- L’administrateur compagnie voit toutes les stations
- Le responsable zone voit les stations autorisées

### Contraintes
- Impossible de supprimer un mouvement validé
- Historique non modifiable
- Toute correction passe par un nouveau mouvement

---


