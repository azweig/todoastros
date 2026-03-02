from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
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
      name = data.get('name', '')
      birth_date = data.get('birth_date', '')
      chinese_sign = data.get('chinese_sign', '')
      vedic_sign = data.get('vedic_sign', '')

      # Validar datos requeridos
      if not sign:
          logger.warning("Solicitud con datos incompletos")
          return jsonify({"error": "Falta el signo zodiacal"}), 400

      # Generar hash para la consulta
      query_data = {
          "sign": sign,
          "name": name,
          "birth_date": birth_date,
          "chinese_sign": chinese_sign,
          "vedic_sign": vedic_sign
      }
      query_hash = get_query_hash(query_data)

      # Verificar si ya existe una respuesta almacenada
      stored_response = get_stored_response(query_hash)
      if stored_response:
          logger.info(f"Usando respuesta almacenada para signo {sign}")
          return jsonify(stored_response)

      # Generar respuesta simulada
      logger.info(f"Generando respuesta simulada para signo {sign}")
      
      # Respuesta simulada para todos los signos
      gemstones_text = f"""
# Gemas y Cristales para {sign}

## 1. Cuarzo Transparente
- **Propiedades**: Claridad, amplificación, equilibrio
- **Beneficios**: Ayuda a clarificar pensamientos y amplifica la energía de otras piedras
- **Uso recomendado**: Meditación, joyería o decoración
- **Combinaciones**: Funciona bien con todas las demás piedras

## 2. Amatista
- **Propiedades**: Calma, intuición, protección
- **Beneficios**: Equilibra emociones y mejora la conexión espiritual
- **Uso recomendado**: Cerca de la cabeza durante el descanso o meditación
- **Combinaciones**: Con cuarzo rosa para amor y compasión

## 3. Turmalina Negra
- **Propiedades**: Protección, enraizamiento, purificación
- **Beneficios**: Absorbe y transforma energías negativas
- **Uso recomendado**: En entradas de hogares u oficinas
- **Combinaciones**: Con cuarzo transparente para amplificar su protección

## 4. Lapislázuli
- **Propiedades**: Sabiduría, verdad, comunicación
- **Beneficios**: Mejora la expresión personal y la búsqueda de conocimiento
- **Uso recomendado**: Colgante cerca de la garganta
- **Combinaciones**: Con amatista para mayor intuición

## 5. Citrino
- **Propiedades**: Abundancia, confianza, energía positiva
- **Beneficios**: Atrae prosperidad y mantiene un estado de ánimo positivo
- **Uso recomendado**: En espacios de trabajo o bolsillos
- **Combinaciones**: Con cuarzo ahumado para manifestación práctica
"""
      
      # Personalizar con el nombre si está disponible
      if name:
          gemstones_text = f"# Gemas y Cristales para {name} ({sign})\n" + gemstones_text.split('\n', 1)[1]
      
      # Preparar respuesta
      response_data = {
          "gemstones_info": gemstones_text,
          "sign": sign,
          "name": name if name else "No especificado",
          "birth_date": birth_date if birth_date else "No especificado",
          "chinese_sign": chinese_sign if chinese_sign else "No especificado",
          "vedic_sign": vedic_sign if vedic_sign else "No especificado",
          "is_mock": True
      }
      
      # Almacenar en la base de datos
      store_response(query_hash, response_data)
      
      logger.info(f"Información simulada sobre gemas generada para {sign}")
      return jsonify(response_data)

  except Exception as e:
      logger.error(f"Error al procesar solicitud: {str(e)}")
      import traceback
      logger.error(f"Traceback: {traceback.format_exc()}")
      return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=5035)
