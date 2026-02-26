from flask import Flask, request, jsonify
import sqlite3
import uuid
import hashlib
import os
import jwt
from datetime import datetime, timedelta
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auth_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("auth_service")

app = Flask(__name__)

# Clave secreta para JWT - en producción usar variable de entorno
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "astrofuturo_secret_key")

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        api_key TEXT UNIQUE NOT NULL,
        user_type TEXT NOT NULL DEFAULT 'free',
        subscription_end_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        service_name TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(user_id, service_name)
    )
    ''')
    
    # Crear usuario admin por defecto si no existe
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "astrofuturo2023")
    
    cursor.execute("SELECT id FROM users WHERE username = ?", (admin_username,))
    if not cursor.fetchone():
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        api_key = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (username, password_hash, api_key, user_type) VALUES (?, ?, ?, ?)",
            (admin_username, password_hash, api_key, "admin")
        )
        cursor.execute(
            "INSERT INTO api_keys (api_key, user_id) VALUES (?, ?)",
            (api_key, cursor.lastrowid)
        )
        logger.info(f"Usuario admin creado con API key: {api_key}")
    
    conn.commit()
    conn.close()

# Función para generar JWT
def generate_jwt(user_id, username, user_type):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id,
        'username': username,
        'user_type': user_type
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Función para verificar API key
def verify_api_key(api_key):
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT u.id, u.user_type, u.subscription_end_date 
        FROM users u 
        JOIN api_keys a ON u.id = a.user_id 
        WHERE a.api_key = ? AND a.is_active = 1
        """, 
        (api_key,)
    )
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return None, None, None
    
    user_id, user_type, subscription_end_date = result
    
    # Verificar si la suscripción ha expirado
    if user_type == 'premium' and subscription_end_date:
        subscription_end = datetime.strptime(subscription_end_date, '%Y-%m-%d')
        if subscription_end < datetime.now():
            # Actualizar a usuario gratuito si expiró
            conn = sqlite3.connect('auth.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET user_type = 'free' WHERE id = ?", 
                (user_id,)
            )
            conn.commit()
            conn.close()
            user_type = 'free'
    
    return user_id, user_type, subscription_end_date

# Función para obtener servicios activos de un usuario
def get_user_services(user_id):
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT service_name FROM user_services WHERE user_id = ? AND is_active = 1", 
        (user_id,)
    )
    services = [row[0] for row in cursor.fetchall()]
    conn.close()
    return services

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    admin_key = data.get('admin_key')
    user_type = data.get('user_type', 'free')  # Por defecto, usuario gratuito
    
    # Solo los administradores pueden crear usuarios premium o admin
    if user_type in ['premium', 'admin'] and admin_key != os.environ.get("ADMIN_KEY", "astrofuturo_admin_key"):
        logger.warning(f"Intento de registro con admin_key inválida: {admin_key}")
        return jsonify({"error": "Admin key inválida"}), 403
    
    if not username or not password:
        return jsonify({"error": "Se requiere nombre de usuario y contraseña"}), 400
    
    try:
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "El nombre de usuario ya existe"}), 409
        
        # Crear nuevo usuario
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        api_key = str(uuid.uuid4())
        
        # Establecer fecha de fin de suscripción para usuarios premium
        subscription_end_date = None
        if user_type == 'premium':
            subscription_end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        cursor.execute(
            "INSERT INTO users (username, password_hash, api_key, user_type, subscription_end_date) VALUES (?, ?, ?, ?, ?)",
            (username, password_hash, api_key, user_type, subscription_end_date)
        )
        
        user_id = cursor.lastrowid
        
        cursor.execute(
            "INSERT INTO api_keys (api_key, user_id) VALUES (?, ?)",
            (api_key, user_id)
        )
        
        # Asignar servicios básicos para usuarios gratuitos
        basic_services = ['zodiac', 'basic_report']
        for service in basic_services:
            cursor.execute(
                "INSERT INTO user_services (user_id, service_name) VALUES (?, ?)",
                (user_id, service)
            )
        
        # Asignar servicios premium para usuarios premium
        if user_type == 'premium':
            premium_services = ['music', 'astronomy', 'weather', 'astro_report', 'news', 'compatibility', 'location_recommendation']
            for service in premium_services:
                cursor.execute(
                    "INSERT INTO user_services (user_id, service_name) VALUES (?, ?)",
                    (user_id, service)
                )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Usuario {username} registrado exitosamente como {user_type}")
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "api_key": api_key,
            "user_type": user_type,
            "subscription_end_date": subscription_end_date
        }), 201
        
    except Exception as e:
        logger.error(f"Error al registrar usuario: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Se requiere nombre de usuario y contraseña"}), 400
    
    try:
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute(
            "SELECT id, api_key, user_type FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            logger.warning(f"Intento de login fallido para usuario: {username}")
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        user_id, api_key, user_type = user
        token = generate_jwt(user_id, username, user_type)
        
        logger.info(f"Login exitoso para usuario: {username}")
        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "api_key": api_key,
            "user_type": user_type
        }), 200
        
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/auth/verify', methods=['POST'])
def verify():
    data = request.get_json()
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({"error": "Se requiere API key"}), 400
    
    user_id, user_type, subscription_end_date = verify_api_key(api_key)
    
    if not user_id:
        logger.warning(f"Verificación de API key fallida: {api_key}")
        return jsonify({"valid": False}), 401
    
    # Obtener servicios activos del usuario
    services = get_user_services(user_id)
    
    logger.info(f"API key verificada para usuario ID: {user_id}, tipo: {user_type}")
    return jsonify({
        "valid": True, 
        "user_id": user_id, 
        "user_type": user_type,
        "subscription_end_date": subscription_end_date,
        "services": services
    }), 200

@app.route('/auth/upgrade', methods=['POST'])
def upgrade_account():
    data = request.get_json()
    api_key = data.get('api_key')
    payment_token = data.get('payment_token')  # Token de confirmación de pago
    
    if not api_key or not payment_token:
        return jsonify({"error": "Se requieren API key y token de pago"}), 400
    
    user_id, user_type, _ = verify_api_key(api_key)
    
    if not user_id:
        logger.warning(f"Verificación de API key fallida: {api_key}")
        return jsonify({"error": "API key inválida"}), 401
    
    if user_type == 'premium':
        return jsonify({"error": "El usuario ya tiene una cuenta premium"}), 400
    
    try:
        # Aquí iría la verificación real del pago con un servicio de pagos
        # Por ahora, simulamos que el pago fue exitoso
        
        # Actualizar tipo de usuario y fecha de fin de suscripción
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()
        
        subscription_end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        cursor.execute(
            "UPDATE users SET user_type = 'premium', subscription_end_date = ? WHERE id = ?",
            (subscription_end_date, user_id)
        )
        
        # Asignar servicios premium
        premium_services = ['music', 'astronomy', 'weather', 'astro_report', 'news', 'compatibility', 'location_recommendation']
        for service in premium_services:
            cursor.execute(
                "INSERT OR IGNORE INTO user_services (user_id, service_name) VALUES (?, ?)",
                (user_id, service)
            )
            cursor.execute(
                "UPDATE user_services SET is_active = 1 WHERE user_id = ? AND service_name = ?",
                (user_id, service)
            )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Usuario ID {user_id} actualizado a premium")
        return jsonify({
            "message": "Cuenta actualizada a premium exitosamente",
            "user_type": "premium",
            "subscription_end_date": subscription_end_date
        }), 200
        
    except Exception as e:
        logger.error(f"Error al actualizar cuenta: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/auth/services', methods=['GET'])
def get_services():
    api_key = request.headers.get('X-API-Key')
    
    if not api_key:
        return jsonify({"error": "Se requiere API key"}), 400
    
    user_id, user_type, _ = verify_api_key(api_key)
    
    if not user_id:
        logger.warning(f"Verificación de API key fallida: {api_key}")
        return jsonify({"error": "API key inválida"}), 401
    
    services = get_user_services(user_id)
    
    return jsonify({
        "user_id": user_id,
        "user_type": user_type,
        "services": services
    }), 200

@app.route('/auth/add_service', methods=['POST'])
def add_service():
    data = request.get_json()
    api_key = data.get('api_key')
    service_name = data.get('service_name')
    payment_token = data.get('payment_token')  # Token de confirmación de pago
    
    if not all([api_key, service_name, payment_token]):
        return jsonify({"error": "Se requieren API key, nombre de servicio y token de pago"}), 400
    
    user_id, user_type, _ = verify_api_key(api_key)
    
    if not user_id:
        logger.warning(f"Verificación de API key fallida: {api_key}")
        return jsonify({"error": "API key inválida"}), 401
    
    try:
        # Aquí iría la verificación real del pago con un servicio de pagos
        # Por ahora, simulamos que el pago fue exitoso
        
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()
        
        # Verificar si el usuario ya tiene el servicio
        cursor.execute(
            "SELECT id FROM user_services WHERE user_id = ? AND service_name = ?",
            (user_id, service_name)
        )
        
        if cursor.fetchone():
            # Actualizar servicio existente
            cursor.execute(
                "UPDATE user_services SET is_active = 1 WHERE user_id = ? AND service_name = ?",
                (user_id, service_name)
            )
        else:
            # Añadir nuevo servicio
            cursor.execute(
                "INSERT INTO user_services (user_id, service_name) VALUES (?, ?)",
                (user_id, service_name)
            )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Servicio {service_name} añadido para usuario ID {user_id}")
        return jsonify({
            "message": f"Servicio {service_name} añadido exitosamente",
            "service_name": service_name
        }), 200
        
    except Exception as e:
        logger.error(f"Error al añadir servicio: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/auth/revoke', methods=['POST'])
def revoke():
    data = request.get_json()
    api_key = data.get('api_key')
    admin_key = data.get('admin_key')
    
    # Verificar que el admin_key es válido
    if admin_key != os.environ.get("ADMIN_KEY", "astrofuturo_admin_key"):
        logger.warning(f"Intento de revocación con admin_key inválida: {admin_key}")
        return jsonify({"error": "Admin key inválida"}), 403
    
    if not api_key:
        return jsonify({"error": "Se requiere API key"}), 400
    
    try:
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE api_keys SET is_active = 0 WHERE api_key = ?",
            (api_key,)
        )
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "API key no encontrada"}), 404
        
        conn.commit()
        conn.close()
        
        logger.info(f"API key revocada: {api_key}")
        return jsonify({"message": "API key revocada exitosamente"}), 200
        
    except Exception as e:
        logger.error(f"Error al revocar API key: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "auth_service"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5050)

