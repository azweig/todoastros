#!/bin/bash

cd /var/html/todoastros

# Matar cualquier proceso de Node.js que pueda estar usando el puerto 3000
echo "Deteniendo cualquier proceso en el puerto 3000..."
fuser -k 3000/tcp 2>/dev/null

# Crear directorio para logs
mkdir -p logs

echo "Iniciando Next.js en modo desarrollo (más fácil para depurar)..."
nohup npm run dev > logs/nextjs.log 2>&1 &

echo "Esperando a que Next.js inicie (10 segundos)..."
sleep 10

# Verificar si Next.js está ejecutándose
if lsof -i:3000 | grep LISTEN > /dev/null; then
  echo "✅ Next.js iniciado correctamente en el puerto 3000"
  echo "Puedes acceder a la aplicación en: http://tu-ip:3000"
else
  echo "❌ Error: Next.js no se inició correctamente."
  echo "Últimas líneas del log:"
  tail -n 20 logs/nextjs.log
fi

