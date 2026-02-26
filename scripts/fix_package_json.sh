#!/bin/bash

# Hacer una copia de seguridad del package.json original
cp package.json package.json.bak

# Modificar el package.json para usar una versión compatible de React
sed -i 's/"react": "\^19"/"react": "^18.2.0"/g' package.json
sed -i 's/"react-dom": "\^19"/"react-dom": "^18.2.0"/g' package.json

echo "package.json actualizado para usar React 18 en lugar de React 19"
echo "Instalando dependencias..."
npm install

echo "Limpiando caché de Next.js..."
rm -rf .next

echo "Construyendo la aplicación..."
npm run build

echo "Iniciando la aplicación..."
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

