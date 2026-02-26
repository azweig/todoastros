#!/bin/bash

echo "Verificando si Next.js está ejecutándose..."
if lsof -i:3000 | grep LISTEN > /dev/null; then
  echo "✅ Next.js está ejecutándose en el puerto 3000"
else
  echo "❌ Next.js NO está ejecutándose en el puerto 3000"
fi

echo -e "\nProcesos de Node.js en ejecución:"
ps aux | grep '[n]ode'

echo -e "\nÚltimas líneas del log de Next.js:"
tail -n 20 logs/nextjs.log

