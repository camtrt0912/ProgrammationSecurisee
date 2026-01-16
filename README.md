# Application Web sécurisée

## Description
Application Flask pour gérer des comptes utilisateurs avec inscription, connexion, espace personnel et rôles.

## Installation
1. Cloner le dépôt
2. Créer un environnement virtuel:
   python -m venv venv
3. Activer le venv:
   venv\Scripts\activate.bat  (Windows)
4. Installer les dépendances:
   python -m pip install flask flask-login flask-wtf
5. Lancer l'application:
   python app.py
6. Ouvrir dans le navigateur:
   http://127.0.0.1:5000

## Fonctionnalités
- Inscription / Connexion
- Dashboard sécurisé
- Gestion des rôles (user/admin)

## Sécurité
- Mots de passe hashés
- Requêtes SQL paramétrées
- Protection XSS
- Protection CSRF
- Sessions sécurisées
- Validation côté serveur

## Limitations
- Pas encore HTTPS
- Pas d’authentification OAuth
