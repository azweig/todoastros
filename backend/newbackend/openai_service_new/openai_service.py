import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

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

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar la salud del servicio."""
    return jsonify({"status": "up"}), 200

@app.route('/generate', methods=['POST'])
def generate_text():
    """Endpoint para generar texto (modo de desarrollo)."""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            logger.warning("Solicitud sin prompt")
            return jsonify({"error": "Falta el prompt"}), 400
        
        logger.info(f"Modo de desarrollo: Generando respuesta simulada para prompt: {prompt[:50]}...")
        
        # Generar una respuesta simulada basada en el prompt
        if "zodiac" in prompt.lower() or "signo" in prompt.lower():
            response_text = f"Análisis astrológico para el signo mencionado en: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        elif "compatibility" in prompt.lower() or "compatibilidad" in prompt.lower():
            response_text = f"Análisis de compatibilidad para los signos mencionados en: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        elif "location" in prompt.lower() or "ubicación" in prompt.lower():
            response_text = f"Recomendaciones de ubicación basadas en: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        elif "house" in prompt.lower() or "casa" in prompt.lower():
            response_text = f"Información sobre casas astrológicas para: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        elif "gemstone" in prompt.lower() or "piedra" in prompt.lower():
            response_text = f"Información sobre gemas y cristales para: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        elif "chart" in prompt.lower() or "carta" in prompt.lower():
            response_text = f"Carta astral generada para: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        elif "news" in prompt.lower() or "noticias" in prompt.lower():
            response_text = f"Noticias astrológicas generadas para: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        else:
            response_text = f"Respuesta generada para: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."
        
        return jsonify({"text": response_text})
    
    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5010)
