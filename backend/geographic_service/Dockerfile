FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask flask-cors requests

EXPOSE 5025

CMD ["python", "geographic_service.py"]
