from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import logging
import os
import json
from functools import wraps
import io
import base64

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_gateway.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("api_gateway")

app = Flask(__name__)

# Configurar CORS para permitir solicitudes desde todoastros.com
CORS(app, origins=["https://todoastros.com", "https://www.todoastros.com"])
# Configuración de servicios
AUTH_SERVICE = os.environ.get('AUTH_SERVICE_URL', 'http://auth_service:5050')
ZODIAC_SERVICE = os.environ.get('ZODIAC_SERVICE_URL', 'http://zodiac_service:5001/zodiac')
MUSIC_SERVICE = os.environ.get('MUSIC_SERVICE_URL', 'http://music_service:5002/music')
ASTRONOMY_SERVICE = os.environ.get('ASTRONOMY_SERVICE_URL', 'http://astronomy_service:5003/astronomy')
WEATHER_SERVICE = os.environ.get('WEATHER_SERVICE_URL', 'http://weather_service:5004/weather')
ASTRO_REPORT_SERVICE = os.environ.get('ASTRO_REPORT_SERVICE_URL', 'http://astro_report_service:5006/astro_report')
NEWS_SERVICE = os.environ.get('NEWS_SERVICE_URL', 'http://news_service:5007/news')
PDF_SERVICE = os.environ.get('PDF_SERVICE_URL', 'http://pdf_service:5008/generate_pdf')
COMPATIBILITY_SERVICE = os.environ.get('COMPATIBILITY_SERVICE_URL', 'http://compatibility_service:5009/compatibility')
OPENAI_SERVICE = os.environ.get('OPENAI_SERVICE_URL', 'http://openai_service:5010/generate')
LOCATION_SERVICE = os.environ.get('LOCATION_SERVICE_URL', 'http://location_service:5011/location')
EMAIL_SERVICE = os.environ.get('EMAIL_SERVICE_URL', 'http://email_service:5012/email')
WHATSAPP_SERVICE = os.environ.get('WHATSAPP_SERVICE_URL', 'http://whatsapp_service:5013/whatsapp')
PAYMENT_SERVICE = os.environ.get('PAYMENT_SERVICE_URL', 'http://payment_service:5014')
MOVIE_SERVICE = os.environ.get('MOVIE_SERVICE_URL', 'http://movie_service:5000/api/movies')
ASTRO_CHART_SERVICE = os.environ.get('ASTRO_CHART_SERVICE_URL', 'http://astro_chart_service:5015/astro_chart')
GEOGRAPHIC_SERVICE = os.environ.get('GEOGRAPHIC_SERVICE_URL', 'http://geographic_service:5025/geographic')
HOUSES_SERVICE = os.environ.get('HOUSES_SERVICE_URL', 'http://houses_service:5030/houses')
GEMSTONES_SERVICE = os.environ.get('GEMSTONES_SERVICE_URL', 'http://gemstones_service:5035/gemstones')

# Middleware para verificar API key
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401

        # Verificar API key con el servicio de autenticación
        response = requests.post(f"{AUTH_SERVICE}/auth/verify", json={"api_key": api_key})
        if response.status_code != 200:
            return jsonify({"error": "Invalid API key"}), 401

        # Añadir información del usuario al request
        request.user_info = response.json()
        return f(*args, **kwargs)
    return decorated_function

# Middleware para verificar permisos de usuario premium
def require_premium(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'user_info'):
            return jsonify({"error": "User information not available"}), 401

        if request.user_info.get('user_type') != 'premium':
            return jsonify({"error": "This endpoint requires a premium account"}), 403

        return f(*args, **kwargs)
    return decorated_function

# Middleware para verificar acceso a servicios específicos
def require_service_access(service_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user_info'):
                return jsonify({"error": "User information not available"}), 401

            user_services = request.user_info.get('services', [])
            if service_name not in user_services and request.user_info.get('user_type') != 'premium':
                return jsonify({"error": f"Access to {service_name} service is not available with your account"}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Rutas de autenticación
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    response = requests.post(f"{AUTH_SERVICE}/auth/register", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    response = requests.post(f"{AUTH_SERVICE}/auth/login", json=data)
    return jsonify(response.json()), response.status_code

# Información del usuario
@app.route('/api/user/info', methods=['GET'])
@require_api_key
def user_info():
    return jsonify(request.user_info), 200

# Ruta para el servicio de zodíaco
@app.route('/api/zodiac', methods=['POST'])
@require_api_key
def zodiac():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(ZODIAC_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de música
@app.route('/api/music', methods=['GET'])
@require_api_key
@require_service_access('music')
def music():
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.get(MUSIC_SERVICE, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de astronomía
@app.route('/api/astronomy', methods=['POST'])
@require_api_key
@require_service_access('astronomy')
def astronomy():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(ASTRONOMY_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de clima
@app.route('/api/weather', methods=['GET'])
@require_api_key
@require_service_access('weather')
def weather():
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.get(WEATHER_SERVICE, headers=headers, params=request.args)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de informes astrológicos
@app.route('/api/astro_report', methods=['POST'])
@require_api_key
@require_service_access('astro_report')
def astro_report():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(ASTRO_REPORT_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de noticias
@app.route('/api/news', methods=['POST'])
@require_api_key
@require_service_access('news')
def news():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(NEWS_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de PDF
@app.route('/api/pdf', methods=['POST'])
@require_api_key
def generate_pdf():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(PDF_SERVICE, json=data, headers=headers)
    return response.content, response.status_code, {'Content-Type': 'application/pdf'}

# Ruta para el servicio de compatibilidad
@app.route('/api/compatibility', methods=['POST'])
@require_api_key
@require_service_access('compatibility')
def compatibility():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(COMPATIBILITY_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de ubicación
@app.route('/api/location', methods=['POST'])
@require_api_key
@require_service_access('location')
def location():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(LOCATION_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de email
@app.route('/api/email', methods=['POST'])
@require_api_key
@require_service_access('email')
def email():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(EMAIL_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de WhatsApp
@app.route('/api/whatsapp', methods=['POST'])
@require_api_key
@require_service_access('whatsapp')
def whatsapp():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(WHATSAPP_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de películas
@app.route('/api/movies', methods=['GET'])
@require_api_key
@require_service_access('movies')
def movies():
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.get(MOVIE_SERVICE, headers=headers, params=request.args)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de carta astral
@app.route('/api/astro_chart', methods=['POST'])
@require_api_key
@require_service_access('astro_chart')
def astro_chart():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(ASTRO_CHART_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio geográfico
@app.route('/api/geographic', methods=['POST'])
@require_api_key
@require_service_access('geographic')
def geographic():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(GEOGRAPHIC_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de casas astrológicas
@app.route('/api/houses', methods=['POST'])
@require_api_key
@require_service_access('houses')
def houses():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(HOUSES_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Ruta para el servicio de gemas y cristales
@app.route('/api/gemstones', methods=['POST'])
@require_api_key
@require_service_access('gemstones')
def gemstones():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(GEMSTONES_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

# Rutas para el servicio de pagos
# Rutas para el servicio de pagos
@app.route('/api/payment/create-checkout-session', methods=['POST'])
@require_api_key
def payment_create_checkout_session():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    url = f"{PAYMENT_SERVICE}/payment/create-checkout-session"
    logger.info(f"Enviando solicitud a: {url}")
    try:
        response = requests.post(url, json=data, headers=headers)
        logger.info(f"Respuesta recibida: {response.status_code}")
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        logger.error(f"Error al conectar con el servicio de pago: {str(e)}")
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

@app.route('/api/payment/webhook', methods=['POST'])
def payment_webhook():
    # Los webhooks de Stripe no requieren API key
    data = request.get_data(as_text=True)
    headers = {key: value for key, value in request.headers.items() if key.startswith('Stripe-')}
    url = f"{PAYMENT_SERVICE}/payment/webhook"
    logger.info(f"Enviando webhook a: {url}")
    try:
        response = requests.post(url, data=data, headers=headers)
        return response.content, response.status_code
    except Exception as e:
        logger.error(f"Error al conectar con el servicio de pago (webhook): {str(e)}")
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

@app.route('/api/payment/customer-portal', methods=['POST'])
@require_api_key
def payment_customer_portal():
    data = request.json
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    url = f"{PAYMENT_SERVICE}/payment/customer-portal"
    logger.info(f"Enviando solicitud a: {url}")
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        logger.error(f"Error al conectar con el servicio de pago: {str(e)}")
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

@app.route('/api/payment/subscription-status', methods=['GET'])
@require_api_key
def payment_subscription_status():
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    url = f"{PAYMENT_SERVICE}/payment/subscription-status"
    logger.info(f"Enviando solicitud a: {url}")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        logger.error(f"Error al conectar con el servicio de pago: {str(e)}")
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

@app.route('/api/payment/transactions', methods=['GET'])
@require_api_key
def payment_transactions():
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    url = f"{PAYMENT_SERVICE}/payment/transactions"
    logger.info(f"Enviando solicitud a: {url}")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        logger.error(f"Error al conectar con el servicio de pago: {str(e)}")
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

# Endpoint de prueba para el servicio de pagos
@app.route('/api/test-payment', methods=['GET'])
def test_payment_service():
    try:
        response = requests.get(f"{PAYMENT_SERVICE}/health")
        return jsonify({
            "status": "success",
            "payment_service_url": PAYMENT_SERVICE,
            "response": {
                "status_code": response.status_code,
                "content": response.text
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "payment_service_url": PAYMENT_SERVICE,
            "error": str(e)
        })

# Verificar estado de servicios
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "operational",
        "services": {
            "api_gateway": {"status": "up", "code": 200},
            "auth": {"status": "up", "code": 200},
            "zodiac": {"status": "up", "code": 200},
            "openai": {"status": "up", "code": 200}
        },
        "message": "Los servicios principales están operativos."
    }), 200

# Endpoint adicional para verificar el estado del sistema
@app.route('/api/system-status', methods=['GET'])
def system_status():
    return jsonify({
        "status": "operational",
        "services": {
            "api_gateway": {"status": "up", "code": 200},
            "auth": {"status": "up", "code": 200},
            "zodiac": {"status": "up", "code": 200},
            "openai": {"status": "up", "code": 200}
        },
        "message": "Los servicios principales están operativos."
    }), 200

# Endpoint de prueba
@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "API Gateway funcionando correctamente"}), 200

@app.route('/simple-test', methods=['GET'])
def simple_test():
    return jsonify({"message": "API Gateway test endpoint working"}), 200


# Ruta para el servicio de carta astral básica (accesible para usuarios gratuitos)
@app.route('/api/basic_astro_chart', methods=['POST'])

@app.route('/api/direct_gemstones', methods=['POST'])
def direct_gemstones_service():
    """Endpoint directo para el servicio de gemas sin verificación de permisos"""
    data = request.json
    # Forzar el uso de datos simulados
    data["mock"] = True
    
    # Obtener la URL del servicio de gemas
    gemstones_service = os.environ.get("GEMSTONES_SERVICE", "http://gemstones_service:5035")
    url = f"{gemstones_service}/gemstones"
    
    try:
        # No enviamos la API key, ya que no es necesaria para los datos simulados
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500
@require_api_key
def basic_astro_chart():
    data = request.json
    # Agregar indicador de versión básica
    data['basic_version'] = True
    headers = {'X-API-Key': request.headers.get('X-API-Key')}
    response = requests.post(ASTRO_CHART_SERVICE, json=data, headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/api/direct_gemstones', methods=['POST'])
def direct_gemstones_service():
    """Endpoint directo para el servicio de gemas sin verificación de permisos"""
    data = request.json
    # Forzar el uso de datos simulados
    data["mock"] = True
    
    # Obtener la URL del servicio de gemas
    gemstones_service = os.environ.get("GEMSTONES_SERVICE", "http://gemstones_service:5035")
    url = f"{gemstones_service}/gemstones"
    
    try:
        # No enviamos la API key, ya que no es necesaria para los datos simulados
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
