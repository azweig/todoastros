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
      logging.FileHandler("astro_report_service.log"),
      logging.StreamHandler()
  ]
)
logger = logging.getLogger("astro_report_service")

app = Flask(__name__)
CORS(app)

# URLs de los servicios
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth_service:5050")
OPENAI_SERVICE_URL = os.environ.get("OPENAI_SERVICE_URL", "http://openai_service:5010/generate")

# Configuración de la base de datos
DB_PATH = "/app/data/responses.db"

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
      # Actualizar el timestamp para que parezca reciente
      if isinstance(response_data, dict) and 'generated_at' in response_data:
          response_data['generated_at'] = datetime.now().isoformat()
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

@app.route('/astro_report', methods=['POST'])
def astro_report():
  """Endpoint para generar un informe astrológico personalizado."""
  try:
      # Obtener datos de la solicitud
      data = request.get_json()
      sign = data.get('sign', '')
      birth_date = data.get('birth_date', '')
      name = data.get('name', '')
      report_type = data.get('report_type', 'general')
      force_refresh = data.get('force_refresh', False)  # Nuevo parámetro
      clear_cache = data.get('clear_cache', False)      # Nuevo parámetro

      # Validar datos requeridos
      if not sign:
          logger.warning("Solicitud con datos incompletos")
          return jsonify({"error": "Falta el signo zodiacal"}), 400

      # Si se solicita borrar la caché, hacerlo antes de continuar
      if clear_cache:
          conn = sqlite3.connect(DB_PATH)
          cursor = conn.cursor()
          cursor.execute("DELETE FROM responses")
          deleted_count = cursor.rowcount
          conn.commit()
          conn.close()
          logger.info(f"Se borraron {deleted_count} entradas de la caché")

      # Generar hash para la consulta
      query_data = {
          "sign": sign,
          "birth_date": birth_date,
          "name": name,
          "report_type": report_type
      }
      query_hash = get_query_hash(query_data)

      # Verificar si ya existe una respuesta almacenada (a menos que se solicite forzar actualización)
      if not force_refresh:
          stored_response = get_stored_response(query_hash)
          if stored_response:
              logger.info(f"Usando respuesta almacenada para {sign}")
              return jsonify(stored_response)

      # Preparar el prompt para OpenAI
      prompt = (
          "Genera un informe astrológico detallado"
      )
      if name:
          prompt += f" para {name}"

      prompt += f", signo zodiacal {sign}"
      if birth_date:
          prompt += f", nacido/a el {birth_date}"

      prompt += (
          f". El informe debe ser de tipo {report_type} y debe incluir: "
          "1. Características generales del signo "
          "2. Fortalezas y desafíos "
          "3. Compatibilidad con otros signos "
          "4. Predicciones para el futuro próximo "
          "5. Consejos para el crecimiento personal "
          "Utiliza un lenguaje accesible pero profundo, "
          "que combine conocimientos astrológicos tradicionales con psicología moderna."
      )

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
          return jsonify({"error": "No se pudo generar el informe astrológico"}), 500

      # Extraer texto generado
      result = response.json()
      report_text = result.get("text", "")
      if not report_text:
          logger.error("No se recibió texto de OpenAI")
          return jsonify({"error": "No se pudo generar el informe astrológico"}), 500

      # Preparar respuesta
      response_data = {
          "report": report_text,
          "sign": sign,
          "name": name if name else "No especificado",
          "birth_date": birth_date if birth_date else "No especificado",
          "report_type": report_type,
          "generated_at": datetime.now().isoformat()
      }

      # Almacenar en la base de datos
      store_response(query_hash, response_data)

      logger.info(f"Informe astrológico generado exitosamente para {sign}")
      return jsonify(response_data)

  except Exception as e:
      logger.error(f"Error al procesar solicitud: {str(e)}")
      import traceback
      logger.error(f"Traceback: {traceback.format_exc()}")
      return jsonify({"error": f"Error interno: {str(e)}"}), 500

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
  """Endpoint para borrar toda la caché."""
  try:
      # Borrar todas las entradas de la base de datos
      conn = sqlite3.connect(DB_PATH)
      cursor = conn.cursor()

      cursor.execute("DELETE FROM responses")

      deleted_count = cursor.rowcount
      conn.commit()
      conn.close()

      logger.info(f"Se borraron {deleted_count} entradas de la caché")
      return jsonify({"success": True, "message": f"Se borraron {deleted_count} entradas de la caché"})

  except Exception as e:
      logger.error(f"Error al borrar caché: {str(e)}")
      import traceback
      logger.error(f"Traceback: {traceback.format_exc()}")
      return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=5006)

