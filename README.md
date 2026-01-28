# Projet : Programmation Sécurisée

**IRA 5 - Projet noté**

## Présentation Générale

Ce projet a pour objectif de concevoir, développer et auditer une application Web de gestion de comptes utilisateurs en appliquant les meilleures pratiques de sécurité applicative.
L'application intègre :

* Un système d'inscription et d'authentification
* Un espace personnel pour chaque utilisateur
* Une gestion des rôles (User/Admin)

---

## Guide d'Installation

Suivez ces étapes pour déployer l'environnement de test localement :

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/camtrt0912/ProgrammationSecurisee.git
   cd ProgrammationSecurisee
   ```

2. **Créer et activer l'environnement virtuel :**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances :**

   ```bash
   pip install flask flask-login flask-wtf email_validator
   ```

4. **Lancer l'application :**

   ```bash
   python app.py
   ```

5. **Accès :**
   Ouvrir votre navigateur à l'adresse : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Description Technique & Sécurité

### 1. Rôle Développeur : Implémentation

Les mécanismes suivants ont été mis en place pour garantir l'intégrité des données et la protection des utilisateurs :

* **Gestion des Mots de Passe :**
  Utilisation de `werkzeug.security` pour le hashage (PBKDF2). Aucun mot de passe n'est stocké en clair.

* **Protection SQL :**
  Requêtes paramétrées via l'ORM/Cursor pour bloquer les injections SQL.

* **Défense CSRF :**
  Intégration de jetons de synchronisation sur tous les formulaires via Flask-WTF.

* **Protection XSS :**
  Échappement automatique des sorties grâce au moteur de template Jinja2 et validation des entrées.

* **Gestion des Sessions :**
  Configuration sécurisée des cookies avec les flags `HttpOnly` et une durée de session limitée.

### 2. Rôle Analyste Sécurité : Audit & Tests

L'application a été soumise à une batterie de tests pour valider les protections :

* **Tests d'injection :** Tentatives infructueuses via des payloads SQL et scripts JS.
* **Audit des sessions :** Vérification de l'impossibilité d'accéder aux cookies via la console (protection HttpOnly).
* **Validation :** Re-tests effectués après chaque correction pour garantir l'absence de vulnérabilités critiques.

---

## Structure du Projet

```
ProgrammationSecurisee/
│
├─ app.py               # Point d'entrée de l'application
├─ requirements.txt     # Dépendances Python
├─ templates/           # Fichiers HTML (Jinja2)
├─ static/              # Fichiers CSS, JS, images
└─ README.md            # Documentation du projet
```

---

## Références

1. Documentation Flask : [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
2. Flask-Login : [https://flask-login.readthedocs.io/](https://flask-login.readthedocs.io/)
3. Flask-WTF : [https://flask-wtf.readthedocs.io/](https://flask-wtf.readthedocs.io/)
4. OWASP Top 10 : [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
5. Sécurité des mots de passe : PBKDF2 & werkzeug.security

---

## Autrice

* Camille TOURET - IRA5
