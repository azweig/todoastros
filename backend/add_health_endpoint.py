#!/usr/bin/env python3

import sys

def add_health_endpoint(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Buscar dónde insertar el nuevo endpoint (justo antes de if __name__ == "__main__")
    if_main_pos = content.find('if __name__ == "__main__"')
    if if_main_pos == -1:
        print("No se pudo encontrar la sección 'if __name__ == \"__main__\"'")
        return False
    
    # Crear el nuevo endpoint
    health_endpoint = '''
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "auth_service"}), 200

'''
    
    # Insertar el nuevo endpoint
    new_content = content[:if_main_pos] + health_endpoint + content[if_main_pos:]
    
    # Guardar el archivo modificado
    with open(file_path, 'w') as file:
        file.write(new_content)
    
    print(f"Endpoint de health check añadido a {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python add_health_endpoint.py <ruta_al_archivo>")
        sys.exit(1)
    
    success = add_health_endpoint(sys.argv[1])
    sys.exit(0 if success else 1)
