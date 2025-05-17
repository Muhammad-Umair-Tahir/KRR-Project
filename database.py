# database.py
import sqlite3
import os
from flask import g

DATABASE_NAME = 'chatbot_users.db'

def get_db():
    """Connects to the specific database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_NAME)
        db.row_factory = sqlite3.Row # Return rows as dictionary-like objects
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    if os.path.exists(DATABASE_NAME):
        print(f"Database '{DATABASE_NAME}' already exists.")
        return

    print("Initializing database...")
    conn = get_db()
    create_tables(conn) # Call function to create tables
    conn.close()
    print("Database initialized successfully.")

def create_tables(conn):
    """Creates the database tables."""
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("Created/Ensured 'users' table.")

    # Create chat_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'bot')),
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    # Added ON DELETE CASCADE so history is removed if user is deleted
    print("Created/Ensured 'chat_history' table.")
    conn.commit()


if __name__ == '__main__':
    # Run this script directly to initialize the database
    init_db()