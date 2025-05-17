import os
import aiml
from autocorrect import spell
from flask import (
    Flask, render_template, request, redirect, url_for, session, flash, g, jsonify
)
from passlib.context import CryptContext
from functools import wraps
import sqlite3
import database
from aipo import initialize, process_question  # Updated logic for AIML + Prolog integration

# --- Configuration ---
BRAIN_FILE = "./pretrained_model/aiml_pretrained_model.dump"
AIML_FILE = "data/family.aiml"
PROLOG_FILE = "prolog/family_relationship.pl"
SECRET_KEY = os.environ.get("SECRET_KEY", "replace-this-with-a-real-secret-key-in-prod")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Chatbot Knowledge Bases (Global) ---
aiml_kernel = None
prolog_kb = None

app = Flask(__name__)
app.secret_key = SECRET_KEY


# --- Initialize AIML and Prolog ---
def initialize_chatbot_systems():
    global aiml_kernel, prolog_kb
    aiml_kernel, prolog_kb = initialize(AIML_FILE, PROLOG_FILE, BRAIN_FILE)
    if aiml_kernel and prolog_kb:
        print("Chatbot systems initialized successfully.")
    else:
        print("Failed to initialize chatbot systems.")
    # Check if both systems are initialized
    return aiml_kernel is not None and prolog_kb is not None


# --- Database Handlers ---
@app.before_request
def before_request():
    try:
        g.db = database.get_db()
    except Exception as e:
        print(f"DB connection error: {e}")
        g.db = None


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# --- Auth Helpers ---
def get_user_by_email(email):
    if not hasattr(g, 'db') or g.db is None: return None
    try:
        return g.db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    except sqlite3.Error as e:
        print(f"get_user_by_email error: {e}")
        return None


def get_user_by_id(user_id):
    if not hasattr(g, 'db') or g.db is None: return None
    try:
        return g.db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    except sqlite3.Error as e:
        print(f"get_user_by_id error: {e}")
        return None


# --- Login Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for('login_page'))
        user = get_user_by_id(session['user_id'])
        if not user:
            session.clear()
            flash("Session expired. Please log in again.", "warning")
            return redirect(url_for('login_page'))
        g.user = user
        return f(*args, **kwargs)
    return decorated_function


# --- Chat History ---
def get_chat_history(user_id):
    if not hasattr(g, 'db') or g.db is None: return []
    try:
        return g.db.execute(
            "SELECT role, message FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC",
            (user_id,)
        ).fetchall()
    except sqlite3.Error as e:
        print(f"get_chat_history error: {e}")
        return []


def add_chat_message(user_id, role, message):
    if not hasattr(g, 'db') or g.db is None:
        print("Database not available, can't add chat message.")
        return
    try:
        g.db.execute(
            "INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)",
            (user_id, role, message)
        )
        g.db.commit()
    except sqlite3.Error as e:
        print(f"add_chat_message error: {e}")
        g.db.rollback()


# --- Routes ---
@app.route("/")
@login_required
def home():
    user_id = session['user_id']
    history = get_chat_history(user_id)
    return render_template("home.html", user=g.user, history=history)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)
        if not user or not pwd_context.verify(password, user['password_hash']):
            flash("Invalid credentials.", "danger")
            return render_template("login.html", email=email)

        session['user_id'] = user['id']
        session['username'] = user['username']
        flash(f"Welcome, {user['username']}!", "success")
        return redirect(url_for('home'))

    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup_page():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        errors = {}
        if not username: errors['username'] = "Username required."
        if not email: errors['email'] = "Email required."
        if not password or len(password) < 6: errors['password'] = "Minimum 6 characters."
        if password != confirm: errors['confirm'] = "Passwords do not match."

        if get_user_by_email(email): errors['email'] = "Email already used."

        if errors:
            return render_template("signup.html", errors=errors)

        hashed = pwd_context.hash(password)
        try:
            g.db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                         (username, email, hashed))
            g.db.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for('login_page'))
        except sqlite3.Error as e:
            g.db.rollback()
            flash("Database error.", "danger")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login_page'))


@app.route("/get")
@login_required
def get_aiml_response():
    query = request.args.get('msg', '').strip()
    if not query:
        return ":("

    user_id = session['user_id']
    add_chat_message(user_id, 'user', query)
    

    if aiml_kernel and prolog_kb:
        response = process_question(query, aiml_kernel, prolog_kb)
    else:
        response = "Sorry, chatbot unavailable."

    add_chat_message(user_id, 'bot', response)
    return response


@app.route("/delete_history", methods=['POST'])
@login_required
def delete_history():
    try:
        g.db.execute("DELETE FROM chat_history WHERE user_id = ?", (session['user_id'],))
        g.db.commit()
        return jsonify(status='success')
    except Exception as e:
        return jsonify(status='error', message=str(e))


if __name__ == '__main__':
    database.init_db()
    if not initialize_chatbot_systems():
        print("Warning: Chatbot failed to initialize.")
    app.run(host='0.0.0.0', port=5000, debug=True)
