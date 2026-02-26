FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
RUN pip install --no-cache-dir flask==2.0.1 werkzeug==2.0.1 requests==2.26.0 pyjwt==2.1.0 billboard.py

# Crear directorio para la base de datos
RUN mkdir -p /app/data

# Copiar el código fuente
COPY . .

# Exponer el puerto
EXPOSE 5002

# Comando para ejecutar la aplicación
CMD ["python", "music_service.py"]
