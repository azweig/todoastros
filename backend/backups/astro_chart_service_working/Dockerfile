FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY astro_chart_service.py .

# Crear directorio para datos
RUN mkdir -p /data

# Exponer el puerto
EXPOSE 5015

CMD ["python", "astro_chart_service.py"]
