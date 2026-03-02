#!/usr/bin/env python3

import sys

def add_test_endpoint(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Buscar la línea donde definir el nuevo endpoint
    insert_line = -1
    for i, line in enumerate(content):
        if 'if __name__ == "__main__"' in line:
            insert_line = i
            break

    if insert_line == -1:
        # Si no encontramos la línea, insertamos al final
        insert_line = len(content)

    # Crear el endpoint de prueba
    test_endpoint = [
        "\n# Endpoint de prueba\n",
        "@app.route('/api/test', methods=['GET'])\n",
        "def test_endpoint():\n",
        "    return jsonify({\"message\": \"API Gateway funcionando correctamente\"}), 200\n\n"
    ]
    
    # Insertar el nuevo endpoint
    content = content[:insert_line] + test_endpoint + content[insert_line:]
    
    # Guardar el archivo modificado
    with open(file_path, 'w') as file:
        file.writelines(content)
    
    print(f"Endpoint de prueba añadido a {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python add_test_endpoint.py <ruta_al_archivo>")
        sys.exit(1)
    
    success = add_test_endpoint(sys.argv[1])
    sys.exit(0 if success else 1)
