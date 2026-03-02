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
      logging.FileHandler("news_service.log"),
      logging.StreamHandler()
  ]
)
logger = logging.getLogger("news_service")

app = Flask(__name__)
CORS(app)

# URLs de los servicios
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth_service:5050")
OPENAI_SERVICE_URL = os.environ.get("OPENAI_SERVICE_URL", "http://openai_service:5010/generate")

# Configuración de la base de datos
DB_PATH = "/app/data/news_responses.db"

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

@app.route('/news', methods=['POST'])
def news():
  """Endpoint para generar noticias astrológicas."""
  try:
      # Obtener datos de la solicitud
      data = request.get_json()
      city_of_birth = data.get('city_of_birth', '')
      date_of_birth = data.get('date_of_birth', '')
      sign = data.get('sign', '')
      category = data.get('category', 'general')

      # Validar datos requeridos
      if not date_of_birth:
          logger.warning("Solicitud con datos incompletos")
          return jsonify({"error": "Falta la fecha de nacimiento"}), 400

      # Generar hash para la consulta
      query_data = {
          "city_of_birth": city_of_birth,
          "date_of_birth": date_of_birth,
          "sign": sign,
          "category": category
      }
      query_hash = get_query_hash(query_data)

      # Verificar si ya existe una respuesta almacenada
      stored_response = get_stored_response(query_hash)
      if stored_response:
          logger.info(f"Usando respuesta almacenada para {date_of_birth} en {city_of_birth}")
          return jsonify(stored_response)

      # Preparar el prompt para OpenAI
      if city_of_birth and date_of_birth:
          prompt = f"""
          Actúa como un experto en futurología y astrología, especializado en brindar mensajes personalizados y reflexivos.
          Quiero que redactes un mensaje especial para alguien nacido el {date_of_birth} en {city_of_birth}.
          1. Si hay eventos históricos o culturales relevantes en esa ciudad en esa fecha, menciónalos de forma que resalten
             la conexión especial entre la persona y su lugar de nacimiento.
          2. Si no hay eventos específicos en la ciudad, enfócate en la singularidad de la persona y en el significado general
             de la fecha en contextos más amplios (nacional o global), siempre resaltando la importancia de la persona.
          3. Evita inventar eventos o mencionar cosas que no existan. Si no hay eventos, enfócate en el simbolismo de la fecha,
             los astros o el impacto positivo de su nacimiento.
          4. Escribe con un tono místico, empático y motivador, como si estuvieras escribiendo un mensaje único y lleno de sabiduría
             para esa persona.
          """
      elif sign:
          prompt = f"""Genera noticias astrológicas recientes y relevantes para el signo zodiacal {sign}.

          Incluye:
          1. Eventos astrológicos recientes que afectan a {sign}
          2. Predicciones para los próximos días
          3. Consejos para aprovechar las energías actuales
          4. Posibles desafíos y cómo superarlos

          Utiliza un lenguaje accesible pero informativo, como si fuera un artículo de noticias astrológicas profesional."""
      else:
          prompt = """Genera un resumen de las noticias astrológicas más importantes y recientes a nivel general.

          Incluye:
          1. Eventos astrológicos significativos recientes (conjunciones, tránsitos, etc.)
          2. Cómo estos eventos afectan a los diferentes signos
          3. Predicciones generales para los próximos días
          4. Consejos para todos los signos durante este período

          Utiliza un lenguaje accesible pero informativo, como si fuera un artículo de noticias astrológicas profesional."""

      # Enviar solicitud a OpenAI
      logger.info(f"Enviando solicitud a OpenAI: {OPENAI_SERVICE_URL}")
      response = requests.post(
          OPENAI_SERVICE_URL,
          json={
              "prompt": prompt,
              "max_tokens": 1000,
              "temperature": 0.7
          }
      )

      # Verificar respuesta
      if response.status_code != 200:
          logger.error(f"Error al llamar a OpenAI: {response.status_code} - {response.text}")
          return jsonify({"error": "No se pudieron generar las noticias astrológicas"}), 500

      # Extraer texto generado
      result = response.json()
      news_text = result.get("text", "")
      if not news_text:
          logger.error("No se recibió texto de OpenAI")
          return jsonify({"error": "No se pudieron generar las noticias astrológicas"}), 500

      # Preparar respuesta
      response_data = {
          "news_summary": news_text,
          "city_of_birth": city_of_birth,
          "date_of_birth": date_of_birth,
          "sign": sign if sign else "Todos los signos",
          "category": category,
          "generated_at": datetime.now().isoformat()
      }

      # Almacenar en la base de datos
      store_response(query_hash, response_data)

      logger.info(f"Noticias astrológicas generadas exitosamente para {date_of_birth} en {city_of_birth}")
      return jsonify(response_data)

  except Exception as e:
      logger.error(f"Error al procesar solicitud: {str(e)}")
      import traceback
      logger.error(f"Traceback: {traceback.format_exc()}")
      return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
  app.run(debug=False, host="0.0.0.0", port=5007)

