#!/bin/bash

# Buscar la sección del servicio openai_service
if grep -q "openai_service:" docker-compose.yml; then
    # Guardar el contenido actual
    cp docker-compose.yml docker-compose.yml.bak
    
    # Reemplazar la configuración del servicio
    sed -i '/openai_service:/,/^[a-z]/ s|build: ./openai_service|build: ./openai_service_mock|' docker-compose.yml
    
    echo "docker-compose.yml actualizado para usar el servicio OpenAI simulado"
else
    echo "No se encontró la sección openai_service en docker-compose.yml"
fi
