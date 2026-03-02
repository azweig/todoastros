from flask import Flask, request, jsonify
import sqlite3
import logging
import requests
import os
import uuid
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("payment_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("payment_service")

app = Flask(__name__)

# URL del servicio de autenticación
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://localhost:5050")

# Configuración de pagos (simulado)
PAYMENT_SECRET_KEY = os.environ.get("PAYMENT_SECRET_KEY", "payment_secret_key_for_simulation")

def verify_api_key(api_key):
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/verify",
            json={"api_key": api_key}
        )
        if response.status_code == 200 and response.json().get("valid"):
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Error al verificar API key: {str(e)}")
        return None

def init_db():
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    
    # Tabla para registro de pagos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payment_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        payment_token TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        transaction_id TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla para precios de servicios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS service_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL,
        description TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Insertar precios por defecto si no existen
    cursor.execute("SELECT COUNT(*) FROM service_prices")
    if cursor.fetchone()[0] == 0:
        services = [
            ("premium_upgrade", 29.99, "Actualización a cuenta premium por 30 días"),
            ("compatibility", 9.99, "Servicio de compatibilidad de pareja"),
            ("location", 9.99, "Servicio de recomendación de lugares"),
            ("music", 4.99, "Servicio de música de tu fecha de nacimiento"),
            ("astronomy", 4.99, "Servicio de astronomía"),
            ("weather", 4.99, "Servicio de clima histórico"),
            ("astro_report", 14.99, "Informe astrológico detallado"),
            ("news", 4.99, "Eventos históricos y mensajes especiales"),
            ("email", 1.99, "Envío de reportes por email"),
            ("whatsapp", 1.99, "Notificaciones por WhatsApp")
        ]
        
        for service in services:
            cursor.execute(
                "INSERT INTO service_prices (service_name, price, description) VALUES (?, ?, ?)",
                service
            )
    
    conn.commit()
    conn.close()

def process_payment(user_id, payment_token, amount, description):
    """
    Simula el procesamiento de un pago.
    En un entorno real, aquí se conectaría con un gateway de pago como Stripe, PayPal, etc.
    """
    try:
        # Generar ID de transacción único
        transaction_id = str(uuid.uuid4())
        
        # Simular verificación de pago
        # En un entorno real, aquí se verificaría el pago con el proveedor
        payment_successful = True
        
        # Registrar el pago en la base de datos
        conn = sqlite3.connect('payments.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO payment_log (user_id, payment_token, amount, description, status, transaction_id) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, payment_token, amount, description, "completed" if payment_successful else "failed", transaction_id)
        )
        conn.commit()
        conn.close()
        
        if payment_successful:
            return True, transaction_id, "Pago procesado exitosamente"
        else:
            return False, transaction_id, "Error al procesar el pago"
    except Exception as e:
        logger.error(f"Error al procesar pago: {str(e)}")
        return False, None, str(e)

def get_service_price(service_name):
    try:
        conn = sqlite3.connect('payments.db')
        cursor = conn.cursor()
        cursor.execute("SELECT price, description FROM service_prices WHERE service_name = ?", (service_name,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0], result[1]
        else:
            return None, "Servicio no encontrado"
    except Exception as e:
        logger.error(f"Error al obtener precio de servicio: {str(e)}")
        return None, str(e)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/payment', methods=['POST'])
def payment():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    user_info = verify_api_key(api_key)
    
    if not user_info:
        logger.warning(f"Intento de acceso con API key inválida: {api_key}")
        return jsonify({"error": "API key inválida o faltante"}), 401
    
    data = request.get_json()
    payment_token = data.get('payment_token')
    service_name = data.get('service_name')

    if not payment_token:
        logger.warning("Solicitud sin token de pago")
        return jsonify({"error": "Falta token de pago"}), 400

    try:
        user_id = user_info.get("user_id")
        
        # Determinar el monto y descripción según el servicio
        if service_name:
            amount, description = get_service_price(service_name)
            if not amount:
                return jsonify({"error": description}), 404
        else:
            # Si no se especifica servicio, asumir actualización a premium
            amount, description = get_service_price("premium_upgrade")
        
        # Procesar el pago
        success, transaction_id, message = process_payment(user_id, payment_token, amount, description)
        
        if success:
            logger.info(f"Pago exitoso para usuario ID {user_id}, servicio: {service_name}")
            return jsonify({
                "message": "Pago procesado exitosamente",
                "transaction_id": transaction_id,
                "amount": amount,
                "description": description
            }), 200
        else:
            logger.error(f"Error en pago para usuario ID {user_id}: {message}")
            return jsonify({"error": f"Error en el pago: {message}"}), 500
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/payment/services', methods=['GET'])
def get_services():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    user_info = verify_api_key(api_key)
    
    if not user_info:
        logger.warning(f"Intento de acceso con API key inválida: {api_key}")
        return jsonify({"error": "API key inválida o faltante"}), 401
    
    try:
        conn = sqlite3.connect('payments.db')
        cursor = conn.cursor()
        cursor.execute("SELECT service_name, price, description FROM service_prices")
        services = [{"name": row[0], "price": row[1], "description": row[2]} for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({"services": services}), 200
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5014)

