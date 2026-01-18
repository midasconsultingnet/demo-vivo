# Processus de déploiement sur Render

## Fichiers requis

Ce projet contient les fichiers nécessaires pour le déploiement sur Render :

- `requirements.txt` - dépendances Python
- `runtime.txt` - version de Python
- `Procfile` - commande de démarrage
- `.gitignore` - fichiers à ignorer

## Étapes de déploiement

### 1. Préparation du projet
Assurez-vous que tous les fichiers sont inclus dans le dépôt Git.

### 2. Création du compte et connexion
- Allez sur https://render.com/
- Connectez-vous avec votre compte GitHub

### 3. Déploiement de l'application
1. Cliquez sur "New +" → "Web Service"
2. Sélectionnez votre dépôt GitHub (demo-vivo)
3. Choisissez la branche (probablement main)
4. Donnez un nom à votre service (ex: successfuel-station)
5. Sélectionnez "Python" comme runtime

### 4. Configuration du service
- Variables d'environnement à ajouter :
  - `SECRET_KEY`: une clé secrète sécurisée
  - `DEBUG`: False (en production)
  - `DATABASE_URL`: fournie automatiquement si vous liez une base de données PostgreSQL

### 5. Commandes de build et de démarrage
- Build command (laissez par défaut ou utilisez) :
  ```
  pip install -r requirements.txt
  python manage.py collectstatic --noinput
  ```
- Start command (spécifiée dans le Procfile) :
  ```
  gunicorn succes_fuel.wsgi:application --bind 0.0.0.0:$PORT
  ```

### 6. Configuration de la base de données
- Sur Render, créez un nouveau "PostgreSQL" via "New +"
- Liez cette base de données à votre service web

### 7. Exécuter les migrations
Après le premier déploiement, vous devrez peut-être exécuter les migrations :
- Via la console Render ou
- En ajoutant une étape de migration dans le processus de déploiement

## Important

- Assurez-vous que votre code ne contient aucune information sensible en clair
- Les variables sensibles doivent être définies comme variables d'environnement sur Render
- Le service sera accessible via une URL générée par Render (ex: https://successfuel-station.onrender.com)

## Configuration supplémentaire requise dans settings.py

Pour que l'application fonctionne correctement sur Render, assurez-vous que votre fichier `succes_fuel/settings.py` contient :

```python
import os
import dj_database_url
from pathlib import Path

# Autoriser tous les hôtes en production
ALLOWED_HOSTS = ['*']

# Configuration pour Whitenoise (pour servir les fichiers statiques)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajouter ceci
    # ... autres middleware ...
]

# Configuration des fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Optionnellement, pour compresser les fichiers statiques
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration de la base de données pour PostgreSQL (Render)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}
```