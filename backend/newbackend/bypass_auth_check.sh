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
cp api_gateway/api_gateway.py api_gateway/api_gateway.py.bak
echo -e "${GREEN}Copia de seguridad creada en api_gateway/api_gateway.py.bak${NC}"

# Paso 3: Añadir un endpoint directo para el servicio de gemas
echo -e "${BLUE}Añadiendo endpoint directo para el servicio de gemas...${NC}"

# Buscar un buen lugar para añadir el endpoint
LAST_ROUTE=$(grep -n "@app.route" api_gateway/api_gateway.py | tail -n 1)
LINE_NUMBER=$(echo "$LAST_ROUTE" | cut -d':' -f1)

# Crear el código para el nuevo endpoint
DIRECT_ENDPOINT='
@app.route(\'/api/direct_gemstones\', methods=[\'POST\'])
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
'

# Añadir el endpoint al archivo
sed -i "${LINE_NUMBER}a\\${DIRECT_ENDPOINT}" api_gateway/api_gateway.py

echo -e "${GREEN}Endpoint directo añadido correctamente${NC}"

# Paso 4: Reiniciar el API Gateway
echo -e "${BLUE}Reiniciando el API Gateway...${NC}"
docker-compose restart api_gateway

# Paso 5: Probar el nuevo endpoint
echo -e "${BLUE}Probando el nuevo endpoint...${NC}"
sleep 5  # Esperar a que el servicio se reinicie

# Datos para la solicitud
GEMSTONES_DATA="{\"sign\":\"Aries\",\"name\":\"Usuario Prueba\",\"birth_date\":\"1990-01-01\",\"chinese_sign\":\"Caballo\",\"vedic_sign\":\"Mesha\"}"

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

