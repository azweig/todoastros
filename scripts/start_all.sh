#!/bin/bash

echo "🚀 Iniciando servicios todoastros..."

# Ruta base
PROJECT_DIR="/var/html/todoastros"
BACKEND="$PROJECT_DIR/backend"
FRONTEND="$PROJECT_DIR/frontend"
LOGS="$PROJECT_DIR/logs"

mkdir -p "$LOGS"

# Servicios Python
declare -A SERVICES=(
  ["astrology_service.py"]=5000
  ["zodiac_service.py"]=5001
  ["music_service.py"]=5002
  ["weather_service.py"]=5004
  ["astro_report_service.py"]=5006
  ["news_service.py"]=5007
)

for SERVICE in "${!SERVICES[@]}"; do
  PORT=${SERVICES[$SERVICE]}
  if [ -f "$BACKEND/$SERVICE" ]; then
    echo "🔧 Iniciando $SERVICE en puerto $PORT"
    nohup python3 "$BACKEND/$SERVICE" > "$LOGS/$SERVICE.log" 2>&1 &
  else
    echo "⚠️  No se encontró: $SERVICE"
  fi
done

# Frontend (Next.js)
echo "🌐 Iniciando frontend (Next.js)"
cd "$FRONTEND"
nohup npm run start > "$LOGS/frontend.log" 2>&1 &

echo "✅ Todos los servicios están iniciados (o en proceso). Revisá logs si hay errores."
