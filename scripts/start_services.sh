#!/bin/bash

# Instalar dependencias
pip3 install -r requirements.txt

# Crear directorio para logs
mkdir -p logs

# Iniciar todos los servicios en segundo plano con nohup
echo "Iniciando servicios..."
nohup python3 zodiac_service.py > logs/zodiac.log 2>&1 &
nohup python3 astronomy_service.py > logs/astronomy.log 2>&1 &
nohup python3 music_service.py > logs/music.log 2>&1 &
nohup python3 weather_service.py > logs/weather.log 2>&1 &
nohup python3 news_service.py > logs/news.log 2>&1 &
nohup python3 astro_report_service.py > logs/astro_report.log 2>&1 &
nohup python3 aggregator_service.py > logs/aggregator.log 2>&1 &

echo "Todos los servicios iniciados en segundo plano."
echo "Los logs se guardan en el directorio 'logs/'."
echo "Para verificar el estado de los servicios, usa: ps aux | grep python3"
echo "Para detener todos los servicios, usa: pkill -f 'python3 *_service.py'"

