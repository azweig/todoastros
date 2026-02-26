FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorio para datos persistentes
RUN mkdir -p /app/data
VOLUME /app/data

CMD ["python", "astro_report_service.py"]

