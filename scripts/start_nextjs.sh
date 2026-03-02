#!/bin/bash

cd /var/html/todoastros

# Instalar dependencias si es necesario
npm install

# Construir la aplicación
npm run build

# Iniciar la aplicación en modo producción
nohup npm start > logs/nextjs.log 2>&1 &

echo "Aplicación Next.js iniciada en segundo plano"
echo "Para verificar los logs: tail -f logs/nextjs.log"

