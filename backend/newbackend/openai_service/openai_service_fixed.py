import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import traceback
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

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

# Configurar OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("No se ha configurado la clave de API de OpenAI. Usando modo de desarrollo.")
    # Usar una clave de API de respaldo para desarrollo
    api_key = "sk-test-key-for-development"

# Crear cliente de OpenAI con modo de desarrollo si no hay clave API
if api_key == "sk-test-key-for-development":
    # En modo de desarrollo, modificar la función generate_text_internal
    def generate_text_internal(prompt, max_tokens=1000, temperature=0.7, model="gpt-3.5-turbo"):
        """Función interna para generar texto en modo de desarrollo."""
        try:
            logger.info(f"Modo de desarrollo: Generando respuesta simulada para prompt: {prompt[:50]}...")
            
            # Generar una respuesta simulada basada en el prompt
            if "zodiac" in prompt.lower() or "signo" in prompt.lower():
                return {"text": f"Análisis astrológico para el signo mencionado en: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."}
            elif "compatibility" in prompt.lower() or "compatibilidad" in prompt.lower():
                return {"text": f"Análisis de compatibilidad para los signos mencionados en: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."}
            else:
                return {"text": f"Respuesta generada para: {prompt[:100]}...\n\nEste es un texto generado en modo de desarrollo."}
                
        except Exception as e:
            logger.error(f"Error al generar texto en modo de desarrollo: {str(e)}")
            return {"text": f"Error en modo de desarrollo: {str(e)}"}
else:
    # Crear cliente de OpenAI con la clave API real
    client = OpenAI(api_key=api_key)
    
    def generate_text_internal(prompt, max_tokens=1000, temperature=0.7, model="gpt-3.5-turbo"):
        """Función interna para generar texto con OpenAI."""
        try:
            # Generar texto con OpenAI
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Eres un astrólogo experto que escribe cartas astrales detalladas y personalizadas."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extraer el texto generado
            generated_text = response.choices[0].message.content
            
            logger.info(f"Texto generado exitosamente: {len(generated_text)} caracteres")
            return {"text": generated_text}

        except Exception as e:
            logger.error(f"Error al generar texto con OpenAI: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Para desarrollo, devolver un texto de ejemplo
            return {"text": f"Texto de ejemplo para el prompt: {prompt[:50]}..."}

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar la salud del servicio."""
    return jsonify({"status": "up"}), 200

@app.route('/generate', methods=['POST'])
def generate_text():
    """Endpoint para generar texto con OpenAI."""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        max_tokens = data.get('max_tokens', 1000)
        temperature = data.get('temperature', 0.7)
        model = data.get('model', 'gpt-3.5-turbo')
        
        if not prompt:
            logger.warning("Solicitud sin prompt")
            return jsonify({"error": "Falta el prompt"}), 400
        
        result = generate_text_internal(prompt, max_tokens, temperature, model)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error al procesar solicitud: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5010)
