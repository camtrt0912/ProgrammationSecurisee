#Camille TOURET
#IRA5
#28/08/2026
import os
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from markupsafe import escape


app = Flask(__name__)
# Protection contre le vol de cookies
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.secret_key = "camilletouret"  

# Chemin de la base de données
DATABASE = os.path.join(os.path.dirname(__file__), "database.db")
print("Chemin complet de la DB :", os.path.abspath(DATABASE))



# Création de la base de données si elle n'existe pas
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Formulaire sécurisé d'inscription
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("S'inscrire")

# Formulaire sécurisé de connexion
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")


# Page d'accueil → redirige vers login
@app.route("/")
def index():
    return redirect("/login")

# Page inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Protection XSS
        email = escape(form.email.data)
        password = form.password.data

        # Hashage sécurisé du mot de passe
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Requête paramétrée = protection SQL Injection
            cursor.execute(
                "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                (email, hashed_password, "user")
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "Email déjà utilisé"

    return render_template("register.html", form=form)


# Page connexion
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        email = escape(form.email.data)
        password = form.password.data

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["role"] = user[3]
            session.permanent = True
            return redirect("/dashboard")
        else:
            error = "Email ou mot de passe incorrect."

    return render_template("login.html", form=form, error=error)


# Dashboard sécurisé
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    # Si l'utilisateur est admin, récupérer la liste de tous les utilisateurs
    users_list = []
    if session["role"] == "admin":
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, role FROM users")
        users_list = cursor.fetchall()
        conn.close()

    return render_template("dashboard.html", role=session["role"], users=users_list)


# Déconnexion
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Gestion des rôles
@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return "Accès interdit"

    return "Bienvenue admin"

# Liste des utilisateurs (accessible uniquement aux admins)
@app.route("/users")
def users():
    if "user_id" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return "Accès interdit"

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, role FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template("users.html", users=users)

# Rajout de mon nom
@app.context_processor
def inject_user():
    return dict(author_name="Camille TOURET")


# Lancement
if __name__ == "__main__":
    app.run(debug=True)
