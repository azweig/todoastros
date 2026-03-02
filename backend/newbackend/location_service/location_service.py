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
      logging.FileHandler("location_service.log"),
      logging.StreamHandler()
  ]
)
logger = logging.getLogger("location_service")

app = Flask(__name__)
CORS(app)

# URLs de los servicios
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth_service:5050")
OPENAI_SERVICE_URL = os.environ.get("OPENAI_SERVICE_URL", "http://openai_service:5010/generate")
ZODIAC_SERVICE_URL = os.environ.get("ZODIAC_SERVICE_URL", "http://zodiac_service:5001/zodiac")

# Configuración de la base de datos
DB_PATH = "/app/data/location_responses.db"

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

@app.route('/location', methods=['POST'])
def location_recommendation():
  try:
      # Obtener datos de la solicitud
      data = request.get_json()
      date_of_birth = data.get('date_of_birth')
      city_of_birth = data.get('city_of_birth')

      if not all([date_of_birth, city_of_birth]):
          logger.warning("Solicitud sin datos obligatorios")
          return jsonify({"error": "Faltan datos obligatorios: date_of_birth, city_of_birth"}), 400

      # Generar hash para la consulta
      query_data = {
          "date_of_birth": date_of_birth,
          "city_of_birth": city_of_birth
      }
      query_hash = get_query_hash(query_data)

      # Verificar si ya existe una respuesta almacenada
      stored_response = get_stored_response(query_hash)
      if stored_response:
          logger.info(f"Usando respuesta almacenada para {date_of_birth} en {city_of_birth}")
          return jsonify(stored_response)

      # Obtener signo zodiacal
      headers = {'X-API-Key': request.headers.get('X-API-Key', '')}

      zodiac_response = requests.post(
          ZODIAC_SERVICE_URL,
          json={"date_of_birth": date_of_birth},
          headers=headers
      )

      if zodiac_response.status_code != 200:
          logger.error("Error al obtener signo zodiacal")
          return jsonify({"error": "Error al obtener signo zodiacal"}), 500

      western_zodiac = zodiac_response.json().get("western_zodiac")
      chinese_zodiac = zodiac_response.json().get("chinese_zodiac")

      # Crear el prompt para OpenAI
      prompt = f"""
      Basándote en la astrología y el feng shui, recomienda 5 lugares ideales para una persona con:

      - Signo zodiacal occidental: {western_zodiac}
      - Signo zodiacal chino: {chinese_zodiac}
      - Lugar de nacimiento: {city_of_birth}
      - Fecha de nacimiento: {date_of_birth}

      Para cada lugar, proporciona:
      1. Nombre del lugar (ciudad o país)
      2. Por qué es adecuado para trabajo/carrera
      3. Por qué es adecuado para relaciones/amor
      4. Mejor época del año para visitarlo

      Formatea la respuesta como un JSON con esta estructura:
      {{
          "recommended_places": [
              {{
                  "name": "Nombre del lugar",
                  "work_compatibility": "Razón para trabajo",
                  "relationship_compatibility": "Razón para relaciones",
                  "best_time": "Mejor época",
                  "description": "Descripción general"
              }},
              ...
          ]
      }}
      """

      # Enviar la solicitud al servicio OpenAI
      openai_response = requests.post(
          OPENAI_SERVICE_URL,
          json={
              "prompt": prompt,
              "max_tokens": 1000,
              "temperature": 0.7
          }
      )

      if openai_response.status_code == 200:
          response_text = openai_response.json().get("text", "").strip()

          # Extraer el JSON de la respuesta
          try:
              # Buscar el inicio y fin del JSON en la respuesta
              start_idx = response_text.find('{')
              end_idx = response_text.rfind('}') + 1
              json_str = response_text[start_idx:end_idx]

              recommendations = json.loads(json_str)
              
              # Preparar respuesta
              response_data = {
                  "date_of_birth": date_of_birth,
                  "city_of_birth": city_of_birth,
                  "western_zodiac": western_zodiac,
                  "chinese_zodiac": chinese_zodiac,
                  "recommendations": recommendations,
                  "generated_at": datetime.now().isoformat()
              }

              # Almacenar en la base de datos
              store_response(query_hash, response_data)

              logger.info(f"Nuevas recomendaciones de lugares generadas y guardadas para {date_of_birth} en {city_of_birth}")
              return jsonify(response_data)
          except json.JSONDecodeError as e:
              logger.error(f"Error al decodificar JSON: {str(e)}, respuesta: {response_text}")
              return jsonify({"error": "Error al procesar la respuesta", "raw_response": response_text}), 500
      else:
          logger.error(f"Error en servicio OpenAI: {openai_response.status_code} - {openai_response.text}")
          return jsonify({"error": f"Error en el servicio OpenAI: {openai_response.text}"}), openai_response.status_code
  except Exception as e:
      logger.error(f"Error: {str(e)}")
      import traceback
      logger.error(f"Traceback: {traceback.format_exc()}")
      return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=5011)

