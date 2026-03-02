from flask import Flask, request, jsonify
import billboard
import sqlite3
import os
import json
import logging
from datetime import datetime, timedelta

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("music_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("music_service")

app = Flask(__name__)

# Configuración de la base de datos
DB_PATH = os.path.join('data', 'music_cache.db')

def init_db():
    """Inicializa la base de datos para la caché de charts."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS charts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chart_name TEXT NOT NULL,
        date TEXT NOT NULL,
        data TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(chart_name, date)
    )
    ''')
    conn.commit()
    conn.close()
    logger.info(f"Base de datos inicializada en {DB_PATH}")

def get_cached_chart(chart_name, date):
    """Obtiene un chart de la caché si existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT data FROM charts WHERE chart_name = ? AND date = ?",
        (chart_name, date)
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        logger.info(f"Chart {chart_name} para la fecha {date} encontrado en caché")
        return json.loads(result[0])
    
    logger.info(f"Chart {chart_name} para la fecha {date} no encontrado en caché")
    return None

def cache_chart(chart_name, date, data):
    """Guarda un chart en la caché."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO charts (chart_name, date, data) VALUES (?, ?, ?)",
            (chart_name, date, json.dumps(data))
        )
        conn.commit()
        logger.info(f"Chart {chart_name} para la fecha {date} guardado en caché")
    except Exception as e:
        logger.error(f"Error al guardar chart en caché: {str(e)}")
    finally:
        conn.close()

def get_billboard_chart(chart_name, date=None):
    """Obtiene un chart de Billboard."""
    try:
        chart = billboard.ChartData(chart_name, date=date)
        
        # Convertir el chart a un formato serializable
        chart_data = {
            "name": chart.name,
            "date": chart.date,
            "entries": []
        }
        
        for entry in chart:
            entry_data = {
                "rank": entry.rank,
                "title": entry.title,
                "artist": entry.artist,
                "image": entry.image if hasattr(entry, 'image') else None,
                "last_week": entry.lastPos if hasattr(entry, 'lastPos') else None,
                "weeks_on_chart": entry.weeks if hasattr(entry, 'weeks') else None,
                "peak_position": entry.peakPos if hasattr(entry, 'peakPos') else None
            }
            chart_data["entries"].append(entry_data)
        
        return chart_data
    except Exception as e:
        logger.error(f"Error al obtener chart de Billboard: {str(e)}")
        return None

@app.route('/charts/<chart_name>', methods=['GET'])
def get_chart(chart_name):
    """Endpoint para obtener un chart específico."""
    date = request.args.get('date')
    
    # Verificar si el chart está en caché
    cached_data = get_cached_chart(chart_name, date)
    
    if cached_data:
        return jsonify(cached_data)
    
    # Si no está en caché, obtenerlo de Billboard
    chart_data = get_billboard_chart(chart_name, date)
    
    if not chart_data:
        return jsonify({"error": "No se pudo obtener el chart"}), 500
    
    # Guardar en caché
    cache_chart(chart_name, date, chart_data)
    
    return jsonify(chart_data)

@app.route('/available_charts', methods=['GET'])
def available_charts():
    """Endpoint para obtener la lista de charts disponibles."""
    charts = [
        {"id": "hot-100", "name": "Hot 100"},
        {"id": "billboard-200", "name": "Billboard 200"},
        {"id": "artist-100", "name": "Artist 100"},
        {"id": "social-50", "name": "Social 50"},
        {"id": "streaming-songs", "name": "Streaming Songs"},
        {"id": "radio-songs", "name": "Radio Songs"},
        {"id": "digital-song-sales", "name": "Digital Song Sales"},
        {"id": "on-demand-streaming-songs", "name": "On-Demand Streaming Songs"},
        {"id": "top-album-sales", "name": "Top Album Sales"},
        {"id": "current-albums", "name": "Current Albums"},
        {"id": "latin-songs", "name": "Hot Latin Songs"},
        {"id": "latin-albums", "name": "Top Latin Albums"}
    ]
    
    return jsonify(charts)

@app.route('/search', methods=['GET'])
def search_music():
    """Endpoint para buscar música por artista o título."""
    query = request.args.get('q')
    chart_name = request.args.get('chart', 'hot-100')
    date = request.args.get('date')
    
    if not query:
        return jsonify({"error": "Se requiere un término de búsqueda"}), 400
    
    # Verificar si el chart está en caché
    cached_data = get_cached_chart(chart_name, date)
    
    if not cached_data:
        # Si no está en caché, obtenerlo de Billboard
        chart_data = get_billboard_chart(chart_name, date)
        
        if not chart_data:
            return jsonify({"error": "No se pudo obtener el chart"}), 500
        
        # Guardar en caché
        cache_chart(chart_name, date, chart_data)
    else:
        chart_data = cached_data
    
    # Buscar en el chart
    results = []
    query = query.lower()
    
    for entry in chart_data["entries"]:
        if query in entry["title"].lower() or query in entry["artist"].lower():
            results.append(entry)
    
    return jsonify({
        "query": query,
        "chart": chart_name,
        "date": chart_data["date"],
        "results": results
    })

@app.route('/artist/<artist_name>', methods=['GET'])
def get_artist_songs(artist_name):
    """Endpoint para obtener canciones de un artista específico."""
    chart_name = request.args.get('chart', 'hot-100')
    date = request.args.get('date')
    
    # Verificar si el chart está en caché
    cached_data = get_cached_chart(chart_name, date)
    
    if not cached_data:
        # Si no está en caché, obtenerlo de Billboard
        chart_data = get_billboard_chart(chart_name, date)
        
        if not chart_data:
            return jsonify({"error": "No se pudo obtener el chart"}), 500
        
        # Guardar en caché
        cache_chart(chart_name, date, chart_data)
    else:
        chart_data = cached_data
    
    # Buscar canciones del artista
    artist_songs = []
    artist_name = artist_name.lower()
    
    for entry in chart_data["entries"]:
        if artist_name in entry["artist"].lower():
            artist_songs.append(entry)
    
    return jsonify({
        "artist": artist_name,
        "chart": chart_name,
        "date": chart_data["date"],
        "songs": artist_songs
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio."""
    return jsonify({"status": "ok", "service": "music_service"}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5002)
