#!/bin/bash

echo "Deteniendo todos los servicios Python..."
pkill -f 'python3 .*_service.py'
echo "Servicios detenidos."

echo "Verificando que no queden servicios en ejecución..."
ps aux | grep '[p]ython3 .*_service.py'

