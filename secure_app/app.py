from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "cle_secrete_a_changer"  # change-le plus tard

DATABASE = "database.db"

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

# Page d'accueil → redirige vers login
@app.route("/")
def index():
    return redirect("/login")

# Page inscription
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if len(password) < 8:
            return "Mot de passe trop court (8 caractères minimum)"

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
        except:
            return "Email déjà utilisé"

    return render_template("register.html")

# Page connexion
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

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

    return render_template("login.html")

# Dashboard sécurisé
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html", role=session["role"])

# Déconnexion
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Lancement
if __name__ == "__main__":
    app.run(debug=True)
