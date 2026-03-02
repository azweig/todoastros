from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("openai_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("openai_service")

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/generate', methods=['POST'])
def generate():
    # Obtener datos de la solicitud
    data = request.get_json()
    prompt = data.get('prompt')
    max_tokens = data.get('max_tokens', 1000)
    temperature = data.get('temperature', 0.7)
    
    # Clave API de OpenAI desde el archivo .env
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Verificar si tenemos una clave API
    if not api_key:
        logger.warning("No se ha configurado la clave de API de OpenAI. Usando modo de desarrollo.")
        # Modo de desarrollo - devolver respuestas simuladas
        if "zodiac" in prompt.lower() or "signo" in prompt.lower():
            response_text = f"Análisis astrológico para el signo mencionado en: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        elif "compatibility" in prompt.lower() or "compatibilidad" in prompt.lower():
            response_text = f"Análisis de compatibilidad para los signos mencionados en: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        elif "chart" in prompt.lower() or "carta" in prompt.lower():
            response_text = f"Carta astral generada para: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        else:
            response_text = f"Respuesta generada para: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        
        return jsonify({"text": response_text})
    
    # URL de la API de OpenAI
    url = "https://api.openai.com/v1/chat/completions"
    
    # Datos para la solicitud
    openai_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Eres un astrólogo experto que escribe cartas astrales detalladas y personalizadas."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    # Cabeceras
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        logger.info(f"Enviando solicitud a OpenAI API: {prompt[:50]}...")
        
        # Realizar la solicitud
        response = requests.post(url, json=openai_data, headers=headers)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            result = response.json()
            text = result['choices'][0]['message']['content']
            logger.info(f"Texto generado exitosamente: {len(text)} caracteres")
            return jsonify({"text": text})
        else:
            logger.error(f"Error en la API de OpenAI: {response.status_code} - {response.text}")
            return jsonify({"error": f"Error en la API de OpenAI: {response.text}"}), response.status_code
    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/openai/generate', methods=['POST'])
def openai_generate():
    return generate()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=False)
