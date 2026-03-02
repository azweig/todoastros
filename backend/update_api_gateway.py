#!/usr/bin/env python3

import sys
import re

def update_api_gateway(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Buscar la última ruta definida antes de if __name__ == "__main__"
    last_route_pattern = re.compile(r'@app\.route$$.*?\n.*?def .*?$$.*?\n', re.DOTALL)
    matches = list(last_route_pattern.finditer(content))
    
    if not matches:
        print("No se encontraron rutas en el archivo")
        return False
    
    last_route = matches[-1]
    last_route_end = last_route.end()
    
    # Crear los nuevos endpoints para el servicio de música
    music_endpoints = '''
# Endpoints para el servicio de música
@app.route('/api/music/charts/<chart_name>', methods=['GET'])
@require_api_key
def get_music_chart(chart_name):
    date = request.args.get('date')
    params = {}
    if date:
        params['date'] = date
    response = requests.get(f"{MUSIC_SERVICE}/charts/{chart_name}", params=params)
    return jsonify(response.json()), response.status_code

@app.route('/api/music/available_charts', methods=['GET'])
@require_api_key
def get_available_charts():
    response = requests.get(f"{MUSIC_SERVICE}/available_charts")
    return jsonify(response.json()), response.status_code

@app.route('/api/music/search', methods=['GET'])
@require_api_key
def search_music():
    query = request.args.get('q')
    chart = request.args.get('chart')
    date = request.args.get('date')
    
    params = {'q': query}
    if chart:
        params['chart'] = chart
    if date:
        params['date'] = date
    
    response = requests.get(f"{MUSIC_SERVICE}/search", params=params)
    return jsonify(response.json()), response.status_code

@app.route('/api/music/artist/<artist_name>', methods=['GET'])
@require_api_key
def get_artist_songs(artist_name):
    chart = request.args.get('chart')
    date = request.args.get('date')
    
    params = {}
    if chart:
        params['chart'] = chart
    if date:
        params['date'] = date
    
    response = requests.get(f"{MUSIC_SERVICE}/artist/{artist_name}", params=params)
    return jsonify(response.json()), response.status_code

'''
    
    # Insertar los nuevos endpoints después de la última ruta
    new_content = content[:last_route_end] + music_endpoints + content[last_route_end:]
    
    # Guardar el archivo modificado
    with open(file_path, 'w') as file:
        file.write(new_content)
    
    print(f"Endpoints de música añadidos a {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python update_api_gateway.py <ruta_al_archivo>")
        sys.exit(1)
    
    success = update_api_gateway(sys.argv[1])
    sys.exit(0 if success else 1)
