#!/bin/bash

# Lista de puertos a liberar
PORTS=(5000 5050 5001 5002 5003 5004 5005 5006 5007 5008 5009 5010)

for port in "${PORTS[@]}"; do
  echo "Verificando puerto $port"
  # Encontrar PID del proceso que usa el puerto
  pid=$(sudo lsof -t -i:$port)
  if [ ! -z "$pid" ]; then
    echo "Matando proceso $pid que usa el puerto $port"
    sudo kill -9 $pid
  else
    echo "Puerto $port está libre"
  fi
done

echo "Todos los puertos han sido liberados"
