#!/bin/bash

echo "Verificando estado de los servicios Python..."
ps aux | grep '[p]ython3 .*_service.py'

echo -e "\nVerificando estado de Next.js..."
ps aux | grep '[n]ode' | grep next

echo -e "\nVerificando puertos..."
for port in 3000 5000 5001 5002 5003 5004 5006 5007; do
  service=$(lsof -i:$port | grep LISTEN)
  if [ -z "$service" ]; then
    echo "Puerto $port: No hay servicio escuchando"
  else
    echo "Puerto $port: $service"
  fi
done

echo -e "\nVerificando configuración de nginx..."
nginx -t

