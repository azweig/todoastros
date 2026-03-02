#!/bin/bash

echo "===== Verificando servicios Python ====="
ps aux | grep '[p]ython3 .*_service.py'

echo -e "\n===== Verificando Next.js ====="
ps aux | grep '[n]ode' | grep next

echo -e "\n===== Verificando puertos ====="
for port in 3000 5000 5001 5002 5003 5004 5006 5007; do
  service=$(lsof -i:$port | grep LISTEN)
  if [ -z "$service" ]; then
    echo "❌ Puerto $port: No hay servicio escuchando"
  else
    echo "✅ Puerto $port: $service"
  fi
done

echo -e "\n===== Verificando nginx ====="
systemctl status nginx | grep Active

echo -e "\n===== Verificando logs de Next.js ====="
tail -n 10 logs/nextjs.log

echo -e "\n===== Verificando logs de nginx ====="
tail -n 10 /var/log/nginx/error.log

