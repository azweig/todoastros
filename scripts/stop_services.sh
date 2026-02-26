#!/bin/bash

echo "Deteniendo todos los servicios..."
pkill -f 'python3 *_service.py'
echo "Servicios detenidos."

