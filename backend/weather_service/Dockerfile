FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY weather_service.py .

# Crear directorio para la base de datos
RUN mkdir -p /data

# Establecer variable de entorno para la ubicación de la base de datos
ENV DB_PATH=/data/weather_data.db

# Exponer el puerto
EXPOSE 5000

CMD ["python", "weather_service.py"]
