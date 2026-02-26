import sqlite3
from flask import Flask, request, jsonify
import logging
import requests
import os
import json
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("astronomy_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("astronomy_service")

app = Flask(__name__)

# URL del servicio de autenticación
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://localhost:5050")

# Ruta de la base de datos astronómica
ASTRO_DB_PATH = os.environ.get("ASTRO_DB_PATH", "/data/astronomical_data.db")
LOCAL_DB_PATH = 'astronomy.db'

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
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()

    # Tabla para eventos astronómicos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS astronomical_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        event_type TEXT NOT NULL,
        details TEXT,
        ra REAL,
        dec REAL,
        UNIQUE(date, event_type)
    )
    ''')

    # Tabla para coordenadas de ciudades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS city_coordinates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        country TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        UNIQUE(city, country)
    )
    ''')

    # Tabla para caché de resultados
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS astronomy_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_of_birth TEXT UNIQUE NOT NULL,
        results TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/astronomy', methods=['POST'])
def astronomy():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        logger.warning(f"Intento de acceso con API key inválida: {api_key}")
        return jsonify({"error": "API key inválida o faltante"}), 401

    data = request.get_json()
    date_of_birth = data.get('date_of_birth')

    if not date_of_birth:
        logger.warning("Solicitud sin fecha de nacimiento")
        return jsonify({"error": "Falta la fecha de nacimiento"}), 400

    try:
        # Verificar si ya existe en caché
        conn_local = sqlite3.connect(LOCAL_DB_PATH)
        cursor_local = conn_local.cursor()
        
        cursor_local.execute(
            "SELECT results FROM astronomy_cache WHERE date_of_birth = ?",
            (date_of_birth,)
        )
        cached = cursor_local.fetchone()

        if cached:
            conn_local.close()
            logger.info(f"Datos astronómicos recuperados de caché para {date_of_birth}")
            return json.loads(cached[0])

        # Consultar la base de datos astronómica
        conn_astro = sqlite3.connect(ASTRO_DB_PATH)
        cursor_astro = conn_astro.cursor()

        # Obtener fase lunar
        cursor_astro.execute(
            "SELECT phase, phase_angle FROM moon_phases WHERE date = ?",
            (date_of_birth,)
        )
        moon_result = cursor_astro.fetchone()
        
        if moon_result:
            moon_phase, phase_angle = moon_result
        else:
            moon_phase = "Desconocido"
            phase_angle = None

        # Obtener posiciones planetarias
        cursor_astro.execute(
            "SELECT planet, ra, dec, distance FROM planetary_positions WHERE date = ?",
            (date_of_birth,)
        )
        planet_results = cursor_astro.fetchall()
        
        planets = []
        for planet, ra, dec, distance in planet_results:
            planets.append({
                "planet": planet,
                "right_ascension": ra,
                "declination": dec,
                "distance": distance,
                "units": {
                    "right_ascension": "hours",
                    "declination": "degrees",
                    "distance": "astronomical units"
                }
            })
        
        conn_astro.close()

        # Crear la respuesta
        response = {
            "date": date_of_birth,
            "moon_phase": {
                "phase": moon_phase,
                "phase_angle": phase_angle
            },
            "planetary_positions": planets
        }

        # Guardar en caché
        cursor_local.execute(
            "INSERT OR REPLACE INTO astronomy_cache (date_of_birth, results) VALUES (?, ?)",
            (date_of_birth, json.dumps(response))
        )
        conn_local.commit()
        conn_local.close()

        logger.info(f"Nuevos datos astronómicos calculados y guardados para {date_of_birth}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error al consultar la base de datos: {str(e)}")
        return jsonify({"error": f"Error al consultar la base de datos: {str(e)}"}), 500

@app.route('/astronomy/planetary_position', methods=['GET'])
def planetary_position():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        return jsonify({"error": "API key inválida o faltante"}), 401

    date = request.args.get('date')
    planet = request.args.get('planet')

    if not date:
        return jsonify({"error": "Se requiere una fecha (formato: YYYY-MM-DD)"}), 400
    
    if not planet:
        return jsonify({"error": "Se requiere especificar un planeta"}), 400

    try:
        conn = sqlite3.connect(ASTRO_DB_PATH)
        cursor = conn.cursor()
        
        # Buscar posición planetaria en la base de datos
        cursor.execute(
            "SELECT ra, dec, distance FROM planetary_positions WHERE date = ? AND planet = ?",
            (date, planet)
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return jsonify({"error": f"No se encontraron datos para {planet} en la fecha {date}"}), 404
        
        ra, dec, distance = result
        
        return jsonify({
            "planet": planet,
            "date": date,
            "right_ascension": ra,
            "declination": dec,
            "distance": distance,
            "units": {
                "right_ascension": "hours",
                "declination": "degrees",
                "distance": "astronomical units"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/astronomy/moon_phase', methods=['GET'])
def moon_phase():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        return jsonify({"error": "API key inválida o faltante"}), 401

    date = request.args.get('date')

    if not date:
        return jsonify({"error": "Se requiere una fecha (formato: YYYY-MM-DD)"}), 400

    try:
        conn = sqlite3.connect(ASTRO_DB_PATH)
        cursor = conn.cursor()
        
        # Buscar fase lunar en la base de datos
        cursor.execute(
            "SELECT phase, phase_angle FROM moon_phases WHERE date = ?",
            (date,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return jsonify({"error": f"No se encontraron datos para la fecha {date}"}), 404
        
        phase, phase_angle = result
        
        return jsonify({
            "date": date,
            "moon_phase": phase,
            "phase_angle": phase_angle
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/astronomy/all_planets', methods=['GET'])
def all_planets():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        return jsonify({"error": "API key inválida o faltante"}), 401

    date = request.args.get('date')

    if not date:
        return jsonify({"error": "Se requiere una fecha (formato: YYYY-MM-DD)"}), 400

    try:
        conn = sqlite3.connect(ASTRO_DB_PATH)
        cursor = conn.cursor()
        
        # Buscar todas las posiciones planetarias para la fecha
        cursor.execute(
            "SELECT planet, ra, dec, distance FROM planetary_positions WHERE date = ?",
            (date,)
        )
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return jsonify({"error": f"No se encontraron datos para la fecha {date}"}), 404
        
        planets = []
        for planet, ra, dec, distance in results:
            planets.append({
                "planet": planet,
                "right_ascension": ra,
                "declination": dec,
                "distance": distance
            })
        
        return jsonify({
            "date": date,
            "planets": planets,
            "units": {
                "right_ascension": "hours",
                "declination": "degrees",
                "distance": "astronomical units"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/astronomy/date_info', methods=['GET'])
def date_info():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        return jsonify({"error": "API key inválida o faltante"}), 401

    date = request.args.get('date')

    if not date:
        return jsonify({"error": "Se requiere una fecha (formato: YYYY-MM-DD)"}), 400

    try:
        # Obtener fase lunar
        conn = sqlite3.connect(ASTRO_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT phase, phase_angle FROM moon_phases WHERE date = ?",
            (date,)
        )
        moon_result = cursor.fetchone()
        
        if not moon_result:
            conn.close()
            return jsonify({"error": f"No se encontraron datos para la fecha {date}"}), 404
        
        moon_phase, phase_angle = moon_result
        
        # Obtener posiciones planetarias
        cursor.execute(
            "SELECT planet, ra, dec, distance FROM planetary_positions WHERE date = ?",
            (date,)
        )
        planet_results = cursor.fetchall()
        
        planets = []
        for planet, ra, dec, distance in planet_results:
            planets.append({
                "planet": planet,
                "right_ascension": ra,
                "declination": dec,
                "distance": distance
            })
        
        conn.close()
        
        return jsonify({
            "date": date,
            "moon_phase": {
                "phase": moon_phase,
                "phase_angle": phase_angle
            },
            "planetary_positions": planets,
            "units": {
                "right_ascension": "hours",
                "declination": "degrees",
                "distance": "astronomical units",
                "phase_angle": "degrees"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5003)
