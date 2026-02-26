from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import requests
import os
import json
import sqlite3
import hashlib
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("gemstones_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("gemstones_service")

app = Flask(__name__)
CORS(app)

# URLs de los servicios
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth_service:5050")
OPENAI_SERVICE_URL = os.environ.get("OPENAI_SERVICE_URL", "http://172.18.0.16:5010/generate")

# Configuración de la base de datos
DB_PATH = "/data/gemstones_responses.db"

def init_db():
    """Inicializa la base de datos."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear tabla para almacenar respuestas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_hash TEXT UNIQUE NOT NULL,
        response_data TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Base de datos inicializada")

def get_query_hash(data):
    """Genera un hash único para la consulta."""
    if isinstance(data, dict):
        # Eliminar campos que no deben afectar el hash (como timestamps)
        data_copy = data.copy()
        if 'generated_at' in data_copy:
            del data_copy['generated_at']
        
        # Convertir a string y generar hash
        data_str = json.dumps(data_copy, sort_keys=True)
    else:
        data_str = str(data)
        
    return hashlib.md5(data_str.encode()).hexdigest()

def get_stored_response(query_hash):
    """Obtiene una respuesta almacenada si existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT response_data FROM responses WHERE query_hash = ?",
        (query_hash,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        response_data = json.loads(result[0])
        return response_data
    
    return None

def store_response(query_hash, response):
    """Almacena una respuesta en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    response_json = json.dumps(response)
    now = datetime.now().isoformat()
    
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO responses (query_hash, response_data, created_at) VALUES (?, ?, ?)",
            (query_hash, response_json, now)
        )
        conn.commit()
        logger.info(f"Respuesta almacenada con hash: {query_hash}")
    except Exception as e:
        logger.error(f"Error al almacenar respuesta: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

# Inicializar la base de datos al arrancar
init_db()

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar la salud del servicio."""
    return jsonify({"status": "up"}), 200

@app.route('/gemstones', methods=['POST'])
def gemstones():
    """Endpoint para obtener información sobre gemas y cristales para un signo zodiacal."""
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        sign = data.get('sign', '')

        # Validar datos requeridos
        if not sign:
            logger.warning("Solicitud con datos incompletos")
            return jsonify({"error": "Falta el signo zodiacal"}), 400

        # Generar hash para la consulta
        query_data = {
            "sign": sign
        }
        query_hash = get_query_hash(query_data)

        # Verificar si ya existe una respuesta almacenada
        stored_response = get_stored_response(query_hash)
        if stored_response:
            logger.info(f"Usando respuesta almacenada para signo {sign}")
            return jsonify(stored_response)

        # Preparar el prompt para OpenAI
        prompt = f"""Proporciona información detallada sobre las gemas y cristales más beneficiosos para el signo zodiacal {sign}.

Para cada gema o cristal, incluye:
1. Nombre de la gema/cristal
2. Propiedades energéticas y metafísicas
3. Cómo beneficia específicamente a {sign}
4. Formas recomendadas de uso (joyería, decoración, meditación, etc.)
5. Combinaciones con otras gemas para potenciar efectos específicos

Incluye al menos 5 gemas o cristales diferentes, ordenados por su nivel de beneficio para {sign}."""

        # Enviar solicitud a OpenAI
        logger.info(f"Enviando solicitud a OpenAI: {OPENAI_SERVICE_URL}")
        response = requests.post(
            OPENAI_SERVICE_URL,
            json={
                "prompt": prompt,
                "max_tokens": 2000,
                "temperature": 0.7
            }
        )

        # Verificar respuesta
        if response.status_code != 200:
            logger.error(f"Error al llamar a OpenAI: {response.status_code} - {response.text}")
            return jsonify({"error": "No se pudo generar la información sobre gemas"}), 500

        # Extraer texto generado
        result = response.json()
        gemstones_text = result.get("text", "")
        if not gemstones_text:
            logger.error("No se recibió texto de OpenAI")
            return jsonify({"error": "No se pudo generar la información sobre gemas"}), 500

        # Preparar respuesta
        response_data = {
            "gemstones_info": gemstones_text,
            "sign": sign
        }

        # Almacenar en la base de datos
        store_response(query_hash, response_data)

        logger.info(f"Información sobre gemas generada exitosamente para {sign}")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5035)
