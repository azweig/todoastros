FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorio para datos persistentes
RUN mkdir -p /data
VOLUME /data

CMD ["python", "compatibility_service.py"]

