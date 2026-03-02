from flask import Flask, request, jsonify
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint simulado para generar texto"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    logger.info(f"Solicitud recibida: {prompt[:100]}...")
    
    # Generar una respuesta simulada
    response_text = """
# Gemas y Cristales Universales (Respuesta Simulada)

## 1. Cuarzo Transparente
- **Propiedades**: Claridad, amplificación, equilibrio
- **Beneficios**: Ayuda a clarificar pensamientos y amplifica la energía de otras piedras
- **Uso recomendado**: Meditación, joyería o decoración
- **Combinaciones**: Funciona bien con todas las demás piedras

## 2. Amatista
- **Propiedades**: Calma, intuición, protección
- **Beneficios**: Equilibra emociones y mejora la conexión espiritual
- **Uso recomendado**: Cerca de la cabeza durante el descanso o meditación
- **Combinaciones**: Con cuarzo rosa para amor y compasión

## 3. Turmalina Negra
- **Propiedades**: Protección, enraizamiento, purificación
- **Beneficios**: Absorbe y transforma energías negativas
- **Uso recomendado**: En entradas de hogares u oficinas
- **Combinaciones**: Con cuarzo transparente para amplificar su protección

## 4. Lapislázuli
- **Propiedades**: Sabiduría, verdad, comunicación
- **Beneficios**: Mejora la expresión personal y la búsqueda de conocimiento
- **Uso recomendado**: Colgante cerca de la garganta
- **Combinaciones**: Con amatista para mayor intuición

## 5. Citrino
- **Propiedades**: Abundancia, confianza, energía positiva
- **Beneficios**: Atrae prosperidad y mantiene un estado de ánimo positivo
- **Uso recomendado**: En espacios de trabajo o bolsillos
- **Combinaciones**: Con cuarzo ahumado para manifestación práctica
"""
    
    return jsonify({"text": response_text})

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar la salud del servicio"""
    return jsonify({"status": "up"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
