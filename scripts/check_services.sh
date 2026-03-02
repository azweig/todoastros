#!/bin/bash

echo "Verificando estado de los servicios..."
ps aux | grep '[p]ython3 .*_service.py'

echo -e "\nVerificando puertos..."
for port in 5000 5001 5002 5003 5004 5006 5007; do
  service=$(lsof -i:$port | grep LISTEN)
  if [ -z "$service" ]; then
    echo "Puerto $port: No hay servicio escuchando"
  else
    echo "Puerto $port: $service"
  fi
done

