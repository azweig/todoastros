#!/usr/bin/env python3

import sys

def add_music_endpoints(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Buscar la línea donde definir los nuevos endpoints
    insert_line = -1
    for i, line in enumerate(content):
        if 'if __name__ == "__main__"' in line:
            insert_line = i
            break

    if insert_line == -1:
        # Si no encontramos la línea, insertamos al final
        insert_line = len(content)

    # Crear los nuevos endpoints para el servicio de música
    music_endpoints = [
        "\n# Endpoints para el servicio de música\n",
        "@app.route('/api/music/charts/<chart_name>', methods=['GET'])\n",
        "@require_api_key\n",
        "def get_music_chart(chart_name):\n",
        "    date = request.args.get('date')\n",
        "    params = {}\n",
        "    if date:\n",
        "        params['date'] = date\n",
        "    response = requests.get(f\"{MUSIC_SERVICE}/charts/{chart_name}\", params=params)\n",
        "    return jsonify(response.json()), response.status_code\n\n",
        
        "@app.route('/api/music/available_charts', methods=['GET'])\n",
        "@require_api_key\n",
        "def get_available_charts():\n",
        "    response = requests.get(f\"{MUSIC_SERVICE}/available_charts\")\n",
        "    return jsonify(response.json()), response.status_code\n\n",
        
        "@app.route('/api/music/search', methods=['GET'])\n",
        "@require_api_key\n",
        "def search_music():\n",
        "    query = request.args.get('q')\n",
        "    chart = request.args.get('chart')\n",
        "    date = request.args.get('date')\n",
        "    \n",
        "    params = {'q': query}\n",
        "    if chart:\n",
        "        params['chart'] = chart\n",
        "    if date:\n",
        "        params['date'] = date\n",
        "    \n",
        "    response = requests.get(f\"{MUSIC_SERVICE}/search\", params=params)\n",
        "    return jsonify(response.json()), response.status_code\n\n",
        
        "@app.route('/api/music/artist/<artist_name>', methods=['GET'])\n",
        "@require_api_key\n",
        "def get_artist_songs(artist_name):\n",
        "    chart = request.args.get('chart')\n",
        "    date = request.args.get('date')\n",
        "    \n",
        "    params = {}\n",
        "    if chart:\n",
        "        params['chart'] = chart\n",
        "    if date:\n",
        "        params['date'] = date\n",
        "    \n",
        "    response = requests.get(f\"{MUSIC_SERVICE}/artist/{artist_name}\", params=params)\n",
        "    return jsonify(response.json()), response.status_code\n\n"
    ]
    
    # Insertar los nuevos endpoints
    content = content[:insert_line] + music_endpoints + content[insert_line:]
    
    # Guardar el archivo modificado
    with open(file_path, 'w') as file:
        file.writelines(content)
    
    print(f"Endpoints de música añadidos a {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python add_music_endpoints.py <ruta_al_archivo>")
        sys.exit(1)
    
    success = add_music_endpoints(sys.argv[1])
    sys.exit(0 if success else 1)
