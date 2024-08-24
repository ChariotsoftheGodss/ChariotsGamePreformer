from flask import Flask, request, jsonify
import sqlite3
import bcrypt

app = Flask(__name__)

# Connect to SQLite databate
def connect_db():
    conn = sqlite3.connect('users.db')
    return conn

# Route for registers a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    username = data['username']
    password = data['password']
    confirm_password = data['confirm+password']

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match!'}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                       (email, username, hashed_password))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User with this email or username already exists!'}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)