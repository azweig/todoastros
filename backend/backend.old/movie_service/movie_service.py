from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Configuración de la API de TMDB
API_KEY = "edf2d3292f4eee8aa076984da1a2f503"
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZGYyZDMyOTJmNGVlZThhYTA3Njk4NGRhMWEyZjUwMyIsIm5iZiI6MTc0MjMxMTQzOC4yODksInN1YiI6IjY3ZDk5MDBlYWIyNTllMDNhN2M2YzBiNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UtO4mO81b_Ih_dJpTubRbbsORXYCFt10OsxVlclrHP4"
BASE_URL = "https://api.themoviedb.org/3"

# Headers para las solicitudes a la API
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json;charset=utf-8"
}

def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/api/movies/discover', methods=['GET'])
@require_api_key
def discover_movies():
    """Obtener películas populares"""
    try:
        page = request.args.get('page', '1')
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                "api_key": API_KEY,
                "language": "es-ES",
                "sort_by": "popularity.desc",
                "include_adult": "false",
                "page": page
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/movies/between_dates', methods=['GET'])
@require_api_key
def movies_between_dates():
    """Obtener películas estrenadas entre dos fechas"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = request.args.get('page', '1')
        
        if not start_date or not end_date:
            return jsonify({"error": "Se requieren fechas de inicio y fin (formato: YYYY-MM-DD)"}), 400
        
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                "api_key": API_KEY,
                "language": "es-ES",
                "sort_by": "popularity.desc",
                "include_adult": "false",
                "page": page,
                "primary_release_date.gte": start_date,
                "primary_release_date.lte": end_date
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/movies/search', methods=['GET'])
@require_api_key
def search_movies():
    """Buscar películas por título"""
    try:
        query = request.args.get('q')
        page = request.args.get('page', '1')
        
        if not query:
            return jsonify({"error": "Se requiere un término de búsqueda"}), 400
        
        response = requests.get(
            f"{BASE_URL}/search/movie",
            headers=HEADERS,
            params={
                "api_key": API_KEY,
                "language": "es-ES",
                "query": query,
                "page": page,
                "include_adult": "false"
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/movies/genres', methods=['GET'])
@require_api_key
def get_genres():
    """Obtener lista de géneros de películas"""
    try:
        response = requests.get(
            f"{BASE_URL}/genre/movie/list",
            headers=HEADERS,
            params={
                "api_key": API_KEY,
                "language": "es-ES"
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/movies/by_genre/<int:genre_id>', methods=['GET'])
@require_api_key
def movies_by_genre(genre_id):
    """Obtener películas por género"""
    try:
        page = request.args.get('page', '1')
        response = requests.get(
            f"{BASE_URL}/discover/movie",
            headers=HEADERS,
            params={
                "api_key": API_KEY,
                "language": "es-ES",
                "sort_by": "popularity.desc",
                "include_adult": "false",
                "page": page,
                "with_genres": genre_id
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/movies/details/<int:movie_id>', methods=['GET'])
@require_api_key
def movie_details(movie_id):
    """Obtener detalles de una película específica"""
    try:
        response = requests.get(
            f"{BASE_URL}/movie/{movie_id}",
            headers=HEADERS,
            params={
                "api_key": API_KEY,
                "language": "es-ES",
                "append_to_response": "credits,videos,images"
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/movies/now_playing', methods=['GET'])
@require_api_key
def now_playing():
    """Obtener películas en cartelera actualmente"""
    try:
        page = request.args.get('page', '1')
        response = requests.get(
            f"{BASE_URL}/movie/now_playing",
            headers=HEADERS,
            params={
                "api_key": API_KEY,
                "language": "es-ES",
                "page": page
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/movies/top_rated', methods=['GET'])
@require_api_key
def top_rated():
    """Obtener películas mejor valoradas"""
    try:
        page = request.args.get('page', '1')
        response = requests.get(
            f"{BASE_URL}/movie/top_rated",
            headers=HEADERS,
            params={
                "api_key": API_KEY,
                "language": "es-ES",
                "page": page
            }
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
