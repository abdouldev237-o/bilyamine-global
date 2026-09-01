# Portfolio — Bilyamine

Site web professionnel complet pour un ingénieur civil / professionnel du bâtiment basé à Douala, Cameroun.

## Stack technique

- **Backend** : Django + Pillow
- **Frontend** : HTML5 + Tailwind CSS (CDN) + Alpine.js (CDN) + JavaScript vanilla
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Langue** : Français

## Installation

### 1. Environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Dépendances

```bash
pip install -r requirements.txt
```

### 3. Base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 5. Données de démonstration (optionnel)

```bash
python manage.py seed_demo
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

Accédez au site : http://127.0.0.1:8000  
Accédez à l'admin : http://127.0.0.1:8000/admin

## Configuration

### Informations du professionnel

Allez dans **Admin > Configuration du site** pour modifier :
- Nom, slogan, présentation
- Téléphones, WhatsApp, email, adresse
- Photo de profil, logo, image hero
- SEO (titre, description, image Open Graph)
- Réseaux sociaux

### Catégories

Allez dans **Admin > Catégories** pour gérer les catégories de réalisations (Maisons, Bâtiments, Rénovation, etc.).

### Services

Allez dans **Admin > Services** pour gérer les services proposés.

### Réalisations

Allez dans **Admin > Réalisations** pour ajouter des projets.  
Vous pouvez ajouter plusieurs images de galerie directement dans la page d'édition d'un projet.

### Témoignages

Les visiteurs peuvent envoyer des témoignages depuis la page publique.  
Allez dans **Admin > Témoignages** pour :
- Approuver, refuser ou remettre en attente
- Mettre à la une
- Voir les badges de statut colorés

**Règle absolue** : un témoignage envoyé par un visiteur est toujours `En attente`. Il n'apparaît publiquement que s'il est `Approuvé`.

## Passage en production

1. Créer un fichier `.env` avec :
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=votredomaine.com`
2. Configurer PostgreSQL dans `config/settings.py`
3. Collecter les fichiers statiques : `python manage.py collectstatic`
4. Configurer un serveur web (Nginx + Gunicorn)

## Contact

Téléphones : +237 693 149 222 / +237 690 892 646 / +237 689 874 206  
WhatsApp : +237 693 149 222
