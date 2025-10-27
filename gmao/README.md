# GMAO Django Application

Ce dépôt contient une application Django de gestion de maintenance assistée par ordinateur (GMAO).  
Vous trouverez ci-dessous les instructions pour lancer le projet en mode local classique ou via Docker, ainsi que les commandes utiles pour les tests.

## Prérequis

- Python 3.12 (recommandé)
- Pip
- (Optionnel) Docker & Docker Compose si vous souhaitez utiliser l'environnement conteneurisé

## Démarrage rapide (environnement local)

1. Cloner le dépôt puis se placer dans le dossier `gmao`.
2. Créer et activer un environnement virtuel :
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # PowerShell
   # source .venv/bin/activate  # macOS / Linux
   ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
4. Appliquer les migrations et créer un superutilisateur :
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Lancer le serveur de développement :
   ```bash
   python manage.py runserver
   ```
6. Accéder à l'application :
   - Accueil : http://127.0.0.1:8000/
   - Administration Django : http://127.0.0.1:8000/admin/

## Lancement avec Docker / Docker Compose

Une configuration simple basée sur SQLite est fournie pour faciliter les tests rapides.

1. Construire l'image et démarrer le conteneur :
   ```bash
   docker compose up --build
   ```
2. Le serveur est disponible sur http://127.0.0.1:8000/.
3. Pour exécuter une commande dans le conteneur (ex. migrations ou shell Django) :
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```
4. Arrêter l'environnement :
   ```bash
   docker compose down
   ```

## Tests automatisés

Lancer les suites de tests disponibles :
```bash
python manage.py test apps.assets apps.users
# ou via Docker :
docker compose exec web python manage.py test
```

## Notes

- Les fichiers médias générés (téléversements) sont stockés dans `media/`.  
- Le mot de passe du superutilisateur doit être modifié après création si vous utilisez l'environnement de test fourni.  
- Le message d'avertissement concernant `django-fsm` provient d'une dépendance transitivement installée ; il est sans incidence pour l'usage standard de l'application.  
- Pour un déploiement en production, il est recommandé d'utiliser une base de données PostgreSQL et un serveur d'application (ex. Gunicorn) derrière un proxy HTTP (ex. Nginx). Le Dockerfile peut servir de base pour ce type d'environnement.
