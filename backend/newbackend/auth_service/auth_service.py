import os
import sqlite3
import hashlib
import logging
from flask import Flask, request, jsonify
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database setup
DATABASE_FILE = 'auth.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            user_type TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    # Create api_keys table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create user_services table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Create a default admin user if it doesn't exist
with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Crear usuario admin por defecto si no existe
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "astrofuturo2023")
    admin_api_key = os.environ.get("ADMIN_KEY", "a56d089d-b0d3-46d7-999e-d2174b04d953")  # Usar la misma clave que en test_flow.py

    cursor.execute("SELECT id FROM users WHERE username = ?", (admin_username,))
    if not cursor.fetchone():
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password_hash, api_key, user_type) VALUES (?, ?, ?, ?)",
            (admin_username, password_hash, admin_api_key, "admin")
        )
        user_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO api_keys (api_key, user_id) VALUES (?, ?)",
            (admin_api_key, user_id)
        )
        logger.info(f"Usuario admin creado con API key: {admin_api_key}")
        
        # Asignar todos los servicios al admin
        all_services = ['zodiac', 'basic_report', 'music', 'astronomy', 'weather', 
                        'astro_report', 'news', 'compatibility', 'location_recommendation',
                        'payment', 'astro_chart', 'gemstones']
        for service in all_services:
            cursor.execute(
                "INSERT INTO user_services (user_id, service_name) VALUES (?, ?)",
                (user_id, service)
            )
        logger.info(f"Servicios asignados al usuario admin")

        conn.commit()
    conn.close()

# Authentication decorator
def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'message': 'API key is missing'}), 401

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM api_keys WHERE api_key = ?", (api_key,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({'message': 'Invalid API key'}), 401

        user_id = result['user_id']
        return f(user_id=user_id, *args, **kwargs)
    return wrapper

# Authorization decorator
def authorize(service_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, user_id=None, **kwargs):
            if user_id is None:
                return jsonify({'message': 'User ID is missing'}), 400

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM user_services WHERE user_id = ? AND service_name = ?", (user_id, service_name))
            result = cursor.fetchone()
            conn.close()

            if not result:
                return jsonify({'message': 'Unauthorized to access this service'}), 403

            return f(*args, user_id=user_id, **kwargs)
        return wrapper
    return decorator

# API Endpoints
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Username already exists'}), 400

    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Generate a unique API key
    api_key = os.urandom(16).hex()

    # Insert the new user into the database
    cursor.execute(
        "INSERT INTO users (username, password_hash, api_key) VALUES (?, ?, ?)",
        (username, password_hash, api_key)
    )
    user_id = cursor.lastrowid

    # Insert the API key into the api_keys table
    cursor.execute(
        "INSERT INTO api_keys (api_key, user_id) VALUES (?, ?)",
        (api_key, user_id)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully', 'api_key': api_key}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the user from the database
    cursor.execute("SELECT id, password_hash, api_key FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    # Verify the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != user['password_hash']:
        return jsonify({'message': 'Invalid username or password'}), 401

    # Return the API key
    return jsonify({'api_key': user['api_key']}), 200

@app.route('/service1')
@authenticate
@authorize('service1')
def service1(user_id):
    return jsonify({'message': f'Service 1 accessed by user {user_id}'})

@app.route('/service2')
@authenticate
@authorize('service2')
def service2(user_id):
    return jsonify({'message': f'Service 2 accessed by user {user_id}'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

