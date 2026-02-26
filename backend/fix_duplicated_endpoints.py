#!/usr/bin/env python3

import sys
import re

def fix_duplicated_endpoints(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Buscar y eliminar los endpoints duplicados
    # Patrón para encontrar los endpoints de música
    pattern = r'(@app\.route$$\'/api/music/.*?\n.*?def .*?$$:\n.*?return jsonify$$response\.json\($$\), response\.status_code\n\n)+'
    
    # Reemplazar los duplicados con una sola instancia
    matches = re.findall(pattern, content, re.DOTALL)
    if matches:
        for match in matches:
            # Contar cuántas veces aparece este bloque
            count = content.count(match)
            if count > 1:
                # Reemplazar todas las ocurrencias excepto la primera
                content = content.replace(match, '', count - 1)
    
    # Guardar el archivo modificado
    with open(file_path, 'w') as file:
        file.write(content)
    
    print(f"Endpoints duplicados eliminados de {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python fix_duplicated_endpoints.py <ruta_al_archivo>")
        sys.exit(1)
    
    success = fix_duplicated_endpoints(sys.argv[1])
    sys.exit(0 if success else 1)
