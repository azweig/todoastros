FROM python:3.9-slim

WORKDIR /app

# Instalar versiones específicas y compatibles
RUN pip install --no-cache-dir flask==2.0.1 werkzeug==2.0.1 flask-cors==3.0.10

COPY openai_service.py .

EXPOSE 5010

CMD ["python", "openai_service.py"]
