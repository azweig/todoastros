@echo off
echo Instalando dependencias...
pip install -r requirements.txt

echo Iniciando servicios...
start python zodiac_service.py
start python astronomy_service.py
start python music_service.py
start python weather_service.py
start python news_service.py
start python astro_report_service.py
start python aggregator_service.py

echo Todos los servicios iniciados. Cierra las ventanas para detenerlos.

