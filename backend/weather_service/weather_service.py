from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import requests
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DB_PATH = os.environ.get('DB_PATH', 'weather_data.db')

def init_db():
    """Inicializa la base de datos si no existe"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla para almacenar datos del clima
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
	country TEXT,
        temperature REAL,
        weather_code INTEGER,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabla para almacenar coordenadas de ciudades
    cursor.execute('''CREATE TABLE IF NOT EXISTS city_coordinates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function



def get_city_coordinates(city):
    """Obtiene las coordenadas de una ciudad desde la base de datos o la API de geocodificación"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Extraer ciudad y país si están separados por coma
    city_parts = city.split(',')
    city_name = city_parts[0].strip()
    country_filter = city_parts[1].strip() if len(city_parts) > 1 else None
    
    # Buscar en la base de datos primero
    if country_filter:
        cursor.execute("SELECT city, latitude, longitude, country FROM city_coordinates WHERE city LIKE ? AND country LIKE ?", 
                      (f"%{city_name}%", f"%{country_filter}%"))
    else:
        cursor.execute("SELECT city, latitude, longitude, country FROM city_coordinates WHERE city LIKE ?", 
                      (f"%{city_name}%",))
    
    result = cursor.fetchone()
    
    if result:
        conn.close()
        return {"city": result[0], "latitude": result[1], "longitude": result[2], "country": result[3]}
    
    # Si no está en la base de datos, usar la API de geocodificación
    try:
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=es&format=json"
        response = requests.get(geocoding_url)
        
        if response.status_code != 200:
            conn.close()
            return None
        
        data = response.json()
        if not data.get("results"):
            conn.close()
            return None
        
        result = data["results"][0]
        latitude = result["latitude"]
        longitude = result["longitude"]
        country = result.get("country", "")
        full_city_name = result.get("name", city_name)
        
        # Guardar en la base de datos para futuras consultas
        cursor.execute(
            "INSERT INTO city_coordinates (city, latitude, longitude, country) VALUES (?, ?, ?, ?)",
            (full_city_name, latitude, longitude, country)
        )
        conn.commit()
        conn.close()
        
        return {"city": full_city_name, "latitude": latitude, "longitude": longitude, "country": country}
    except Exception as e:
        conn.close()
        print(f"Error al obtener coordenadas: {str(e)}")
        return None


def get_weather_code_description(code):
    """Mapea códigos de clima de Open-Meteo a descripciones en español"""
    weather_conditions = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        66: "Lluvia fría ligera",
        67: "Lluvia fría intensa",
        71: "Nevada ligera",
        73: "Nevada moderada",
        75: "Nevada intensa",
        77: "Granos de nieve",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos intensos",
        85: "Chubascos de nieve ligeros",
        86: "Chubascos de nieve intensos",
        95: "Tormenta eléctrica",
        96: "Tormenta eléctrica con granizo ligero",
        99: "Tormenta eléctrica con granizo intenso"
    }
    return weather_conditions.get(code, "Desconocido")

@app.route('/weather/historical', methods=['GET'])
@require_api_key
def historical_weather():
    """Obtiene datos históricos del clima para una fecha y ubicación específicas"""
    try:
        date = request.args.get('date')
        city = request.args.get('city')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not date:
            return jsonify({"error": "Se requiere una fecha (formato: YYYY-MM-DD)"}), 400
        
        # Validar formato de fecha
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
        
        # Obtener coordenadas si se proporciona una ciudad
        if city and not (lat and lon):
            coordinates = get_city_coordinates(city)
            if not coordinates:
                return jsonify({"error": f"No se encontraron coordenadas para la ciudad: {city}"}), 404
            lat = coordinates["latitude"]
            lon = coordinates["longitude"]
        
        if not (lat and lon):
            return jsonify({"error": "Se requiere ciudad o coordenadas (lat/lon)"}), 400
        
        # Verificar si ya tenemos los datos en la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT temperature, weather_code, description FROM weather_data WHERE date = ? AND latitude = ? AND longitude = ?",
            (date, lat, lon)
        )
        cached_data = cursor.fetchone()
        
        if cached_data:
            conn.close()
            return jsonify({
                "date": date,
                "latitude": float(lat),
                "longitude": float(lon),
                "temperature": cached_data[0],
                "weather_code": cached_data[1],
                "description": cached_data[2],
                "source": "cache"
            })
        
        # Si no está en caché, consultar la API de Open-Meteo
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date}&end_date={date}&daily=temperature_2m_mean,weathercode&timezone=auto"
        response = requests.get(url)
        
        if response.status_code != 200:
            conn.close()
            return jsonify({"error": f"Error al obtener datos de Open-Meteo: {response.text}"}), response.status_code
        
        data = response.json()
        daily_data = data.get("daily", {})
        
        if not daily_data or not daily_data.get("temperature_2m_mean") or len(daily_data["temperature_2m_mean"]) == 0:
            conn.close()
            return jsonify({"error": "No se encontraron datos climáticos para la fecha proporcionada"}), 404
        
        temperature = daily_data["temperature_2m_mean"][0]
        weather_code = daily_data["weathercode"][0]
        description = get_weather_code_description(weather_code)
        
        # Guardar en la base de datos para futuras consultas
        cursor.execute(
            "INSERT INTO weather_data (date, latitude, longitude, temperature, weather_code, description) VALUES (?, ?, ?, ?, ?, ?)",
            (date, lat, lon, temperature, weather_code, description)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            "date": date,
            "latitude": float(lat),
            "longitude": float(lon),
            "temperature": temperature,
            "weather_code": weather_code,
            "description": description,
            "source": "api"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather/current', methods=['GET'])
@require_api_key
def current_weather():
    """Obtiene el clima actual para una ubicación"""
    try:
        city = request.args.get('city')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        # Obtener coordenadas si se proporciona una ciudad
        if city and not (lat and lon):
            coordinates = get_city_coordinates(city)
            if not coordinates:
                return jsonify({"error": f"No se encontraron coordenadas para la ciudad: {city}"}), 404
            lat = coordinates["latitude"]
            lon = coordinates["longitude"]
        
        if not (lat and lon):
            return jsonify({"error": "Se requiere ciudad o coordenadas (lat/lon)"}), 400
        
        # Consultar la API de Open-Meteo para el clima actual
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weathercode,windspeed_10m,winddirection_10m,relative_humidity_2m&timezone=auto"
        response = requests.get(url)
        
        if response.status_code != 200:
            return jsonify({"error": f"Error al obtener datos de Open-Meteo: {response.text}"}), response.status_code
        
        data = response.json()
        current_data = data.get("current", {})
        
        if not current_data:
            return jsonify({"error": "No se encontraron datos climáticos actuales"}), 404
        
        weather_code = current_data.get("weathercode")
        description = get_weather_code_description(weather_code)
        
        result = {
            "temperature": current_data.get("temperature_2m"),
            "weather_code": weather_code,
            "description": description,
            "wind_speed": current_data.get("windspeed_10m"),
            "wind_direction": current_data.get("winddirection_10m"),
            "humidity": current_data.get("relative_humidity_2m"),
            "latitude": float(lat),
            "longitude": float(lon),
            "units": data.get("current_units", {})
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather/forecast', methods=['GET'])
@require_api_key
def weather_forecast():
    """Obtiene el pronóstico del clima para los próximos días"""
    try:
        city = request.args.get('city')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        days = request.args.get('days', '7')
        
        # Obtener coordenadas si se proporciona una ciudad
        if city and not (lat and lon):
            coordinates = get_city_coordinates(city)
            if not coordinates:
                return jsonify({"error": f"No se encontraron coordenadas para la ciudad: {city}"}), 404
            lat = coordinates["latitude"]
            lon = coordinates["longitude"]
        
        if not (lat and lon):
            return jsonify({"error": "Se requiere ciudad o coordenadas (lat/lon)"}), 400
        
        # Consultar la API de Open-Meteo para el pronóstico
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max&timezone=auto&forecast_days={days}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return jsonify({"error": f"Error al obtener datos de Open-Meteo: {response.text}"}), response.status_code
        
        data = response.json()
        daily_data = data.get("daily", {})
        
        if not daily_data:
            return jsonify({"error": "No se encontraron datos de pronóstico"}), 404
        
        # Formatear los datos del pronóstico
        forecast = []
        for i in range(len(daily_data.get("time", []))):
            weather_code = daily_data["weathercode"][i]
            forecast.append({
                "date": daily_data["time"][i],
                "temperature_max": daily_data["temperature_2m_max"][i],
                "temperature_min": daily_data["temperature_2m_min"][i],
                "precipitation_sum": daily_data["precipitation_sum"][i],
                "precipitation_probability": daily_data["precipitation_probability_max"][i],
                "weather_code": weather_code,
                "description": get_weather_code_description(weather_code)
            })
        
        result = {
            "latitude": float(lat),
            "longitude": float(lon),
            "timezone": data.get("timezone", "UTC"),
            "units": data.get("daily_units", {}),
            "forecast": forecast
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather/geocoding', methods=['GET'])
@require_api_key
def geocoding():
    """Convierte nombres de ciudades a coordenadas geográficas"""
    try:
        city = request.args.get('city')
        
        if not city:
            return jsonify({"error": "Se requiere un nombre de ciudad"}), 400
        
        # Verificar si ya tenemos las coordenadas en la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        city_name = city.split(',')[0].strip()
        cursor.execute("SELECT city, latitude, longitude FROM city_coordinates WHERE city LIKE ?", (f"%{city_name}%",))
        results = cursor.fetchall()
        
        if results:
            cities = [{"city": row[0], "latitude": row[1], "longitude": row[2]} for row in results]
            conn.close()
            return jsonify({"results": cities, "source": "cache"})
        
        # Si no está en la base de datos, usar la API de geocodificación
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=5&language=es&format=json"
        response = requests.get(geocoding_url)
        
        if response.status_code != 200:
            conn.close()
            return jsonify({"error": f"Error al obtener datos de geocodificación: {response.text}"}), response.status_code
        
        data = response.json()
        if not data.get("results"):
            conn.close()
            return jsonify({"error": f"No se encontraron resultados para: {city}"}), 404
        
        # Guardar resultados en la base de datos
        for result in data["results"]:
            full_city_name = f"{result.get('name', '')}, {result.get('country', '')}"
            cursor.execute(
                "INSERT INTO city_coordinates (city, latitude, longitude) VALUES (?, ?, ?)",
                (full_city_name, result["latitude"], result["longitude"])
            )
        
        conn.commit()
        conn.close()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather/birth', methods=['POST'])
@require_api_key
def birth_weather():
    """Obtiene el clima en la fecha y lugar de nacimiento"""
    try:
        data = request.get_json()
        date_of_birth = data.get('date_of_birth')
        city_of_birth = data.get('city_of_birth')
        
        if not all([date_of_birth, city_of_birth]):
            return jsonify({"error": "Faltan datos obligatorios (date_of_birth, city_of_birth)"}), 400
        
        # Obtener coordenadas de la ciudad
        coordinates = get_city_coordinates(city_of_birth)
        if not coordinates:
            return jsonify({"error": f"No se encontraron coordenadas para la ciudad: {city_of_birth}"}), 404
        
        lat = coordinates["latitude"]
        lon = coordinates["longitude"]
        
        # Verificar si ya tenemos los datos en la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT temperature, weather_code, description FROM weather_data WHERE date = ? AND latitude = ? AND longitude = ?",
            (date_of_birth, lat, lon)
        )
        cached_data = cursor.fetchone()
        
        if cached_data:
            conn.close()
            return jsonify({
                "date": date_of_birth,
                "city": city_of_birth,
                "latitude": lat,
                "longitude": lon,
                "temperature": cached_data[0],
                "weather_code": cached_data[1],
                "description": cached_data[2],
                "source": "cache"
            })
        
        # Si no está en caché, consultar la API de Open-Meteo
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date_of_birth}&end_date={date_of_birth}&daily=temperature_2m_mean,weathercode&timezone=auto"
        response = requests.get(url)
        
        if response.status_code != 200:
            conn.close()
            return jsonify({"error": f"Error al obtener datos de Open-Meteo: {response.text}"}), response.status_code
        
        data = response.json()
        daily_data = data.get("daily", {})
        
        if not daily_data or not daily_data.get("temperature_2m_mean") or len(daily_data["temperature_2m_mean"]) == 0:
            conn.close()
            return jsonify({"error": "No se encontraron datos climáticos para la fecha proporcionada"}), 404
        
        temperature = daily_data["temperature_2m_mean"][0]
        weather_code = daily_data["weathercode"][0]
        description = get_weather_code_description(weather_code)
        
        # Guardar en la base de datos para futuras consultas
        cursor.execute(
            "INSERT INTO weather_data (date, latitude, longitude, temperature, weather_code, description) VALUES (?, ?, ?, ?, ?, ?)",
            (date_of_birth, lat, lon, temperature, weather_code, description)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            "date": date_of_birth,
            "city": city_of_birth,
            "latitude": lat,
            "longitude": lon,
            "temperature": temperature,
            "weather_code": weather_code,
            "description": description,
            "source": "api"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.before_first_request
def before_first_request():
    """Inicializa la base de datos antes de la primera solicitud"""
    init_db()

if __name__ == '__main__':
    # Asegurarse de que la base de datos esté inicializada
    init_db()
    app.run(host='0.0.0.0', port=5004, debug=True)
