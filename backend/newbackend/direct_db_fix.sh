#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== CORRIGIENDO PERMISOS DIRECTAMENTE EN LA BASE DE DATOS ===${NC}"

# Verificar si el contenedor está en ejecución
CONTAINER_RUNNING=$(docker-compose ps auth_service | grep Up)

if [ -z "$CONTAINER_RUNNING" ]; then
    echo -e "${RED}El contenedor auth_service no está en ejecución${NC}"
    exit 1
fi

# Ejecutar comandos SQL directamente en el contenedor
echo -e "${BLUE}Ejecutando comandos SQL directamente en el contenedor...${NC}"

echo -e "${YELLOW}1. Verificando usuarios administradores:${NC}"
docker-compose exec -T auth_service sqlite3 auth.db "SELECT id, username, user_type FROM users WHERE user_type='admin';"

echo -e "${YELLOW}2. Verificando servicios disponibles:${NC}"
docker-compose exec -T auth_service sqlite3 auth.db "SELECT DISTINCT service_name FROM user_services;"

echo -e "${YELLOW}3. Verificando permisos actuales de los administradores:${NC}"
docker-compose exec -T auth_service sqlite3 auth.db "SELECT u.id, u.username, us.service_name FROM users u JOIN user_services us ON u.id = us.user_id WHERE u.user_type='admin';"

echo -e "${YELLOW}4. Añadiendo servicio de gemas a todos los administradores:${NC}"
docker-compose exec -T auth_service sqlite3 auth.db "INSERT OR IGNORE INTO user_services (user_id, service_name) SELECT id, 'gemstones' FROM users WHERE user_type='admin';"

echo -e "${YELLOW}5. Verificando permisos después de los cambios:${NC}"
docker-compose exec -T auth_service sqlite3 auth.db "SELECT u.id, u.username, us.service_name FROM users u JOIN user_services us ON u.id = us.user_id WHERE u.user_type='admin' AND us.service_name='gemstones';"

# Reiniciar el servicio de autenticación
echo -e "${BLUE}Reiniciando servicio de autenticación...${NC}"
docker-compose restart auth_service

echo -e "${GREEN}Permisos corregidos. Ahora deberías poder acceder al servicio de gemas.${NC}"
echo -e "${BLUE}Prueba el servicio con: ./test_gemstones_mock.sh${NC}"

