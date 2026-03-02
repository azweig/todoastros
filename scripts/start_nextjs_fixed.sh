#!/bin/bash

cd /var/html/todoastros

# Crear directorio para logs si no existe
mkdir -p logs

echo "Instalando dependencias con --legacy-peer-deps para evitar conflictos..."
npm install --legacy-peer-deps

echo "Construyendo la aplicación..."
npm run build

echo "Iniciando la aplicación en modo producción..."
PORT=3000 nohup npm start > logs/nextjs.log 2>&1 &

echo "Esperando a que Next.js inicie..."
sleep 5

# Verificar si Next.js está ejecutándose
if lsof -i:3000 | grep LISTEN > /dev/null; then
  echo "✅ Next.js iniciado correctamente en el puerto 3000"
else
  echo "❌ Error: Next.js no se inició correctamente. Revisa los logs: tail -f logs/nextjs.log"
fi

