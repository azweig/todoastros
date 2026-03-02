#!/usr/bin/env python3

import sys
import re

def update_music_endpoints(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Actualizar los endpoints de música para usar la URL completa
    content = content.replace('f"{MUSIC_SERVICE}/charts/{chart_name}"', '"http://music_service:5002/charts/" + chart_name')
    content = content.replace('f"{MUSIC_SERVICE}/available_charts"', '"http://music_service:5002/available_charts"')
    content = content.replace('f"{MUSIC_SERVICE}/search"', '"http://music_service:5002/search"')
    content = content.replace('f"{MUSIC_SERVICE}/artist/{artist_name}"', '"http://music_service:5002/artist/" + artist_name')
    
    # Guardar el archivo modificado
    with open(file_path, 'w') as file:
        file.write(content)
    
    print(f"Endpoints de música actualizados en {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python update_music_endpoints.py <ruta_al_archivo>")
        sys.exit(1)
    
    success = update_music_endpoints(sys.argv[1])
    sys.exit(0 if success else 1)
