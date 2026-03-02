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
        logging.FileHandler("astro_report_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("astro_report_service")

app = Flask(__name__)
CORS(app)

# URLs de los servicios
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth_service:5050")
OPENAI_SERVICE_URL = os.environ.get("OPENAI_SERVICE_URL", "http://172.18.0.16:5010/generate")

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar la salud del servicio."""
    return jsonify({"status": "up"}), 200

@app.route('/astro_report', methods=['POST'])
def astro_report():
    """Endpoint para generar un informe astrológico personalizado."""
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        sign = data.get('sign', '')
        birth_date = data.get('birth_date', '')
        name = data.get('name', '')
        report_type = data.get('report_type', 'general')

        # Validar datos requeridos
        if not sign:
            logger.warning("Solicitud con datos incompletos")
            return jsonify({"error": "Falta el signo zodiacal"}), 400

        # Preparar el prompt para OpenAI
        prompt = f"""Genera un informe astrológico detallado"""
        
        if name:
            prompt += f" para {name}"
        
        prompt += f", signo zodiacal {sign}"
        
        if birth_date:
            prompt += f", nacido/a el {birth_date}"
            
        prompt += f". El informe debe ser de tipo {report_type} y debe incluir: 1. Características generales del signo 2. Fortalezas y desafíos 3. Compatibilidad con otros signos 4. Predicciones para el futuro próximo 5. Consejos para el crecimiento personal Utiliza un lenguaje accesible pero profundo, que combine conocimientos astrológicos tradicionales con psicología moderna."""

        # Enviar solicitud a OpenAI
        logger.info(f"Enviando solicitud a OpenAI: {OPENAI_SERVICE_URL}")
        response = requests.post(
            OPENAI_SERVICE_URL,
            json={
                "prompt": prompt,
                "max_tokens": 2000,
                "temperature": 0.7
            }
        )

        # Verificar respuesta
        if response.status_code != 200:
            logger.error(f"Error al llamar a OpenAI: {response.status_code} - {response.text}")
            return jsonify({"error": "No se pudo generar el informe astrológico"}), 500

        # Extraer texto generado
        result = response.json()
        report_text = result.get("text", "")
        if not report_text:
            logger.error("No se recibió texto de OpenAI")
            return jsonify({"error": "No se pudo generar el informe astrológico"}), 500

        # Preparar respuesta
        response = {
            "report": report_text,
            "sign": sign,
            "name": name if name else "No especificado",
            "birth_date": birth_date if birth_date else "No especificado",
            "report_type": report_type,
            "generated_at": datetime.now().isoformat()
        }

        logger.info(f"Informe astrológico generado exitosamente para {sign}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5006)
