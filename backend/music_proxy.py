#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("music_proxy.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("music_proxy")

app = Flask(__name__)

# URL del servicio de música
MUSIC_SERVICE = "http://localhost:6002"

@app.route('/api/music/charts/<chart_name>', methods=['GET'])
def get_music_chart(chart_name):
    date = request.args.get('date')
    params = {}
    if date:
        params['date'] = date
    
    logger.info(f"Proxying request to {MUSIC_SERVICE}/charts/{chart_name} with params {params}")
    
    try:
        response = requests.get(f"{MUSIC_SERVICE}/charts/{chart_name}", params=params)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logger.error(f"Error proxying request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/music/available_charts', methods=['GET'])
def get_available_charts():
    logger.info(f"Proxying request to {MUSIC_SERVICE}/available_charts")
    
    try:
        response = requests.get(f"{MUSIC_SERVICE}/available_charts")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logger.error(f"Error proxying request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/music/search', methods=['GET'])
def search_music():
    query = request.args.get('q')
    chart = request.args.get('chart')
    date = request.args.get('date')
    
    params = {'q': query}
    if chart:
        params['chart'] = chart
    if date:
        params['date'] = date
    
    logger.info(f"Proxying request to {MUSIC_SERVICE}/search with params {params}")
    
    try:
        response = requests.get(f"{MUSIC_SERVICE}/search", params=params)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logger.error(f"Error proxying request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/music/artist/<artist_name>', methods=['GET'])
def get_artist_songs(artist_name):
    chart = request.args.get('chart')
    date = request.args.get('date')
    
    params = {}
    if chart:
        params['chart'] = chart
    if date:
        params['date'] = date
    
    logger.info(f"Proxying request to {MUSIC_SERVICE}/artist/{artist_name} with params {params}")
    
    try:
        response = requests.get(f"{MUSIC_SERVICE}/artist/{artist_name}", params=params)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logger.error(f"Error proxying request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "music_proxy"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000)
