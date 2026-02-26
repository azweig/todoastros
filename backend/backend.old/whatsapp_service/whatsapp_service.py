from flask import Flask, request, jsonify
import requests
import logging
import os
import sqlite3
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("whatsapp_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("whatsapp_service")

app = Flask(__name__)

# URL del servicio de autenticación
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://localhost:5050")

# Configuración de WhatsApp (usando WhatsApp Business API)
WHATSAPP_API_URL = os.environ.get("WHATSAPP_API_URL", "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages")
WHATSAPP_API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN", "YOUR_WHATSAPP_API_TOKEN")

def verify_api_key(api_key):
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/verify",
            json={"api_key": api_key}
        )
        return response.status_code == 200 and response.json().get("valid", False)
    except Exception as e:
        logger.error(f"Error al verificar API key: {str(e)}")
        return False

def init_db():
    conn = sqlite3.connect('whatsapp.db')
    cursor = conn.cursor()
    
    # Tabla para registro de mensajes enviados
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS whatsapp_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        to_number TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT NOT NULL,
        error_message TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def send_whatsapp(to_number, message):
    try:
        # Asegurarse de que el número tenga el formato correcto (con código de país)
        if not to_number.startswith('+'):
            to_number = '+' + to_number
        
        # Preparar payload para WhatsApp Business API
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_number,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        headers = {
            "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # En un entorno de producción, descomentar esto:
        # response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
        # if response.status_code == 200:
        #     return True, "Mensaje enviado exitosamente"
        # else:
        #     return False, f"Error al enviar mensaje: {response.text}"
        
        # Para desarrollo/pruebas, simulamos éxito:
        logger.info(f"Simulando envío de WhatsApp a {to_number}: {message}")
        return True, "Mensaje enviado exitosamente (simulado)"
    except Exception as e:
        logger.error(f"Error al enviar WhatsApp: {str(e)}")
        return False, str(e)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        logger.warning(f"Intento de acceso con API key inválida: {api_key}")
        return jsonify({"error": "API key inválida o faltante"}), 401
    
    data = request.get_json()
    to_number = data.get('to')
    message = data.get('message')

    if not all([to_number, message]):
        logger.warning("Solicitud sin datos obligatorios")
        return jsonify({"error": "Faltan datos obligatorios: to, message"}), 400

    try:
        # Enviar WhatsApp
        success, result_message = send_whatsapp(to_number, message)
        
        # Registrar en la base de datos
        conn = sqlite3.connect('whatsapp.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO whatsapp_log (to_number, message, status, error_message) VALUES (?, ?, ?, ?)",
            (to_number, message, "success" if success else "error", None if success else result_message)
        )
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"WhatsApp enviado exitosamente a {to_number}")
            return jsonify({"message": "WhatsApp enviado exitosamente"}), 200
        else:
            logger.error(f"Error al enviar WhatsApp a {to_number}: {result_message}")
            return jsonify({"error": f"Error al enviar WhatsApp: {result_message}"}), 500
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5013)

