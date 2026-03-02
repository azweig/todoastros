FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorio para datos persistentes
RUN mkdir -p /app/data
VOLUME /app/data

# Cambiar al directorio de datos para las bases de datos
WORKDIR /app/data

# Volver al directorio de la aplicación
WORKDIR /app

CMD ["python", "news_service.py"]

