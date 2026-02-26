from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import requests
import os
import json
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("astro_chart_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("astro_chart_service")

app = Flask(__name__)
CORS(app)

# URLs de los servicios
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth_service:5050")
ASTRONOMY_SERVICE_URL = os.environ.get("ASTRONOMY_SERVICE_URL", "http://astronomy_service:5003/astronomy")
ZODIAC_SERVICE_URL = os.environ.get("ZODIAC_SERVICE_URL", "http://zodiac_service:5001/zodiac")
OPENAI_SERVICE_URL = os.environ.get("OPENAI_SERVICE_URL", "http://172.18.0.16:5010/generate")

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar la salud del servicio."""
    return jsonify({"status": "up"}), 200

@app.route('/astro_chart', methods=['POST'])
def astro_chart():
    """Endpoint para generar una carta astral personalizada."""
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        birth_date = data.get('birth_date', '')
        birth_time = data.get('birth_time', '')
        birth_place = data.get('birth_place', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        # Validar datos requeridos
        if not all([birth_date, birth_time, birth_place]):
            logger.warning("Solicitud con datos incompletos")
            return jsonify({"error": "Faltan datos obligatorios (fecha, hora o lugar de nacimiento)"}), 400

        # Preparar el prompt para OpenAI
        name_str = ""
        if first_name and last_name:
            name_str = f" para {first_name} {last_name}"
        elif first_name:
            name_str = f" para {first_name}"

        prompt = f"""Genera una carta astral detallada{name_str} basada en los siguientes datos:
- Fecha de nacimiento: {birth_date}
- Hora de nacimiento: {birth_time}
- Lugar de nacimiento: {birth_place}

La carta astral debe incluir:
1. Análisis del Sol, Luna y Ascendente
2. Posiciones planetarias en signos y casas
3. Aspectos planetarios significativos
4. Interpretación de la personalidad y potencial de vida
5. Desafíos y oportunidades según la carta natal
6. Consejos para el desarrollo personal basados en la carta

Utiliza un lenguaje accesible pero profundo, que combine conocimientos astrológicos tradicionales con psicología moderna."""

        # Enviar solicitud a OpenAI
        logger.info(f"Enviando solicitud a OpenAI: {OPENAI_SERVICE_URL}")
        response = requests.post(
            OPENAI_SERVICE_URL,
            json={
                "prompt": prompt,
                "max_tokens": 2500,
                "temperature": 0.7
            }
        )

        # Verificar respuesta
        if response.status_code != 200:
            logger.error(f"Error al llamar a OpenAI: {response.status_code} - {response.text}")
            return jsonify({"error": "No se pudo generar la carta astral"}), 500

        # Extraer texto generado
        result = response.json()
        chart_text = result.get("text", "")
        if not chart_text:
            logger.error("No se recibió texto de OpenAI")
            return jsonify({"error": "No se pudo generar la carta astral"}), 500

        # Preparar respuesta
        response = {
            "chart": chart_text,
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_place": birth_place,
            "first_name": first_name,
            "last_name": last_name,
            "generated_at": datetime.now().isoformat()
        }

        logger.info(f"Carta astral generada exitosamente para {birth_date}, {birth_time}, {birth_place}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5015)
