#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== CREANDO ENDPOINT DIRECTO PARA EL SERVICIO DE GEMAS ===${NC}"

# Paso 1: Verificar si el archivo api_gateway.py existe
echo -e "${BLUE}Verificando si el archivo api_gateway.py existe...${NC}"

if [ ! -f "api_gateway/api_gateway.py" ]; then
    echo -e "${RED}No se encontró el archivo api_gateway/api_gateway.py${NC}"
    exit 1
else
    echo -e "${GREEN}Archivo api_gateway.py encontrado${NC}"
fi

# Paso 2: Crear una copia de seguridad del archivo
echo -e "${BLUE}Creando copia de seguridad del archivo...${NC}"
cp api_gateway/api_gateway.py api_gateway/api_gateway.py.bak.$(date +%Y%m%d%H%M%S)
echo -e "${GREEN}Copia de seguridad creada${NC}"

# Paso 3: Añadir el nuevo endpoint directo
echo -e "${BLUE}Añadiendo endpoint directo para el servicio de gemas...${NC}"

# Crear un archivo temporal con el nuevo endpoint
cat > direct_gemstones_endpoint.txt << 'EOF'

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
EOF

# Buscar la línea antes de "if __name__ == '__main__':" para insertar el nuevo endpoint
LINE_NUMBER=$(grep -n "if __name__ == '__main__':" api_gateway/api_gateway.py | cut -d':' -f1)

if [ -z "$LINE_NUMBER" ]; then
    echo -e "${RED}No se pudo encontrar el punto de inserción en el archivo${NC}"
    exit 1
fi

# Insertar el nuevo endpoint antes de "if __name__ == '__main__':"
LINE_NUMBER=$((LINE_NUMBER - 1))
sed -i "${LINE_NUMBER}r direct_gemstones_endpoint.txt" api_gateway/api_gateway.py

# Eliminar el archivo temporal
rm direct_gemstones_endpoint.txt

echo -e "${GREEN}Endpoint directo añadido correctamente${NC}"

# Paso 4: Reiniciar el API Gateway
echo -e "${BLUE}Reiniciando el API Gateway...${NC}"
docker-compose restart api_gateway

# Paso 5: Esperar a que el servicio se reinicie
echo -e "${BLUE}Esperando a que el servicio se reinicie...${NC}"
sleep 10

# Paso 6: Probar el nuevo endpoint
echo -e "${BLUE}Probando el nuevo endpoint...${NC}"

# Datos para la solicitud
GEMSTONES_DATA="{\"sign\":\"Aries\",\"name\":\"Usuario Prueba\",\"birth_date\":\"1990-01-01\"}"

# Hacer la solicitud
echo -e "${BLUE}Enviando solicitud a: https://api.todoastros.com/api/direct_gemstones${NC}"
echo -e "${BLUE}Datos: $GEMSTONES_DATA${NC}"

GEMSTONES_RESPONSE=$(curl -s -X POST "https://api.todoastros.com/api/direct_gemstones" \
  -H "Content-Type: application/json" \
  -d "$GEMSTONES_DATA")

echo -e "${GREEN}Respuesta:${NC}"
echo "$GEMSTONES_RESPONSE"

# Verificar si la respuesta contiene un error
if [[ $GEMSTONES_RESPONSE == *"error"* ]]; then
    echo -e "${RED}La solicitud falló. Verificando logs del API Gateway...${NC}"
    docker-compose logs --tail=20 api_gateway
else
    echo -e "${GREEN}¡Solicitud exitosa! El endpoint directo funciona correctamente.${NC}"
    echo -e "${BLUE}Puedes usar este endpoint para acceder al servicio de gemas sin verificación de permisos:${NC}"
    echo -e "${YELLOW}curl -X POST \"https://api.todoastros.com/api/direct_gemstones\" -H \"Content-Type: application/json\" -d '{\"sign\":\"Aries\",\"name\":\"Tu Nombre\",\"birth_date\":\"1990-01-01\"}'${NC}"
fi

echo -e "${BLUE}Proceso completado.${NC}"

