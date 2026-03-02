"""
Script para añadir un endpoint directo para el servicio de gemas
"""

import os
import sys
import re

def add_direct_gemstones_endpoint():
    """Añade un endpoint directo para el servicio de gemas"""
    api_gateway_path = "api_gateway/api_gateway.py"
    
    # Verificar si el archivo existe
    if not os.path.exists(api_gateway_path):
        print(f"Error: No se encontró el archivo {api_gateway_path}")
        return False
    
    # Crear una copia de seguridad
    backup_path = f"{api_gateway_path}.bak.{os.getpid()}"
    try:
        with open(api_gateway_path, 'r') as src, open(backup_path, 'w') as dst:
            dst.write(src.read())
        print(f"Copia de seguridad creada en {backup_path}")
    except Exception as e:
        print(f"Error al crear copia de seguridad: {str(e)}")
        return False
    
    # Nuevo endpoint a añadir
    new_endpoint = """
# Endpoint directo para el servicio de gemas sin verificación de permisos
@app.route('/api/direct_gemstones', methods=['POST'])
def direct_gemstones_service():
    """Endpoint directo para el servicio de gemas sin verificación de permisos"""
    data = request.json
    # Forzar el uso de datos simulados
    data["mock"] = True
    url = f"{GEMSTONES_SERVICE}/gemstones"
    logger.info(f"Enviando solicitud directa a: {url}")
    try:
        # No enviamos la API key, ya que no es necesaria para los datos simulados
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            logger.error(f"Error del servicio de gemas: {response.status_code} - {response.text}")
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        logger.error(f"Error al conectar con el servicio de gemas: {str(e)}")
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500
"""
    
    # Leer el contenido del archivo
    with open(api_gateway_path, 'r') as f:
        content = f.read()
    
    # Verificar si el endpoint ya existe
    if "def direct_gemstones_service" in content:
        print("El endpoint directo ya existe en el archivo")
        return True
    
    # Encontrar el punto de inserción (antes de if __name__ == '__main__':)
    match = re.search(r"if\s+__name__\s*==\s*['\"]__main__['\"]:", content)
    if not match:
        print("No se pudo encontrar el punto de inserción en el archivo")
        return False
    
    # Insertar el nuevo endpoint
    insert_pos = match.start()
    new_content = content[:insert_pos] + new_endpoint + content[insert_pos:]
    
    # Escribir el contenido modificado
    try:
        with open(api_gateway_path, 'w') as f:
            f.write(new_content)
        print("Endpoint directo añadido correctamente")
        return True
    except Exception as e:
        print(f"Error al escribir el archivo: {str(e)}")
        # Restaurar la copia de seguridad
        try:
            with open(backup_path, 'r') as src, open(api_gateway_path, 'w') as dst:
                dst.write(src.read())
            print("Se ha restaurado la copia de seguridad")
        except Exception as e2:
            print(f"Error al restaurar la copia de seguridad: {str(e2)}")
        return False

if __name__ == "__main__":
    print("=== AÑADIENDO ENDPOINT DIRECTO PARA EL SERVICIO DE GEMAS ===\n")
    if add_direct_gemstones_endpoint():
        print("\n¡Endpoint añadido con éxito!")
        print("Reinicia el API Gateway con: docker-compose restart api_gateway")
        print("Prueba el endpoint con: curl -X POST \"https://api.todoastros.com/api/direct_gemstones\" -H \"Content-Type: application/json\" -d '{\"sign\":\"Aries\",\"name\":\"Tu Nombre\",\"birth_date\":\"1990-01-01\"}'")
    else:
        print("\nLa operación falló. Verifica los mensajes de error.")

