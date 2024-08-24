import sqlite3
import bcrypt

def create_connection():
    return sqlite3.connect('users.db')

def create_user_table():
    conn = create_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY, email TEXT, username TEXT, password TEXT)''')

def register_user(email, username, password):
    conn = create_connection()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with conn:
        conn.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                     (email, username, hashed_password))

def verify_user_credentials(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    # Retrieve the stored password hash for the given email
    cursor.execute("SELECT password FROM users WHERE email = ?", (username,))
    row = cursor.fetchone()

    if row:
        stored_password_hash = row[0]

        # Check if the hashed input password matches the stored hash
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            return True

    return False