from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import sqlite3

# -------------------------------
# Configuration Flask
# -------------------------------
app = Flask(__name__)
app.secret_key = "change_cette_cle_pour_la_prod"

# Sécurité des sessions
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

DATABASE = "database.db"

# -------------------------------
# Formulaires Flask-WTF (CSRF)
# -------------------------------
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("S'inscrire")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField("Se connecter")

# -------------------------------
# Base SQL
# -------------------------------
def init_db():
    """Créer la table users si elle n'existe pas"""
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

# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def index():
    return redirect("/login")

# -------------------------------
# Inscription
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = escape(form.email.data)  # Échappe pour sécurité XSS
        password = form.password.data
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                (email, hashed_password, "user")
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Email déjà utilisé"
    return render_template("register.html", form=form)

# -------------------------------
# Connexion
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
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
            return redirect("/dashboard")
        else:
            return "Identifiants incorrects"
    return render_template("login.html", form=form)

# -------------------------------
# Dashboard sécurisé
# -------------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html", role=session["role"])

# -------------------------------
# Déconnexion
# -------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------------------------------
# Lancement
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
