#!/bin/bash

echo "Deteniendo forzosamente todos los servicios Python..."
# Detener servicios en cumpleanos_estelares
pkill -9 -f '/var/html/cumpleanos_estelares/.*_service.py'
# Detener servicios en el directorio actual
pkill -9 -f 'python3 .*_service.py'

echo "Verificando que no queden servicios en ejecución..."
ps aux | grep '[p]ython3 .*_service.py'

