from flask import Flask, request, jsonify, send_file
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

# Configuración de servicios
AUTH_SERVICE = os.environ.get('AUTH_SERVICE', 'http://auth_service:5050')
ZODIAC_SERVICE = os.environ.get('ZODIAC_SERVICE', 'http://zodiac_service:5001')
MUSIC_SERVICE = os.environ.get('MUSIC_SERVICE', 'http://music_service:5002')
ASTRONOMY_SERVICE = os.environ.get('ASTRONOMY_SERVICE', 'http://astronomy_service:5003')
WEATHER_SERVICE = os.environ.get('WEATHER_SERVICE', 'http://weather_service:5004')
ASTRO_REPORT_SERVICE = os.environ.get('ASTRO_REPORT_SERVICE', 'http://astro_report_service:5006')
NEWS_SERVICE = os.environ.get('NEWS_SERVICE', 'http://news_service:5007')
PDF_SERVICE = os.environ.get('PDF_SERVICE', 'http://pdf_service:5008')
COMPATIBILITY_SERVICE = os.environ.get('COMPATIBILITY_SERVICE', 'http://compatibility_service:5009')
OPENAI_SERVICE = os.environ.get('OPENAI_SERVICE', 'http://openai_service:5010')
LOCATION_SERVICE = os.environ.get('LOCATION_SERVICE', 'http://location_service:5011')
EMAIL_SERVICE = os.environ.get('EMAIL_SERVICE', 'http://email_service:5012')
WHATSAPP_SERVICE = os.environ.get('WHATSAPP_SERVICE', 'http://whatsapp_service:5013')
PAYMENT_SERVICE = os.environ.get('PAYMENT_SERVICE', 'http://payment_service:5014')

# Middleware para verificar API key
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401
        
        # Verificar API key con el servicio de autenticación
        response = requests.get(f"{AUTH_SERVICE}/verify_key/{api_key}")
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
    response = requests.post(f"{AUTH_SERVICE}/register", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    response = requests.post(f"{AUTH_SERVICE}/login", json=data)
    return jsonify(response.json()), response.status_code

# Información del usuario
@app.route('/api/user/info', methods=['GET'])
@require_api_key
def user_info():
    return jsonify(request.user_info), 200

# Actualizar a premium
@app.route('/api/user/upgrade', methods=['POST'])
@require_api_key
def upgrade_user():
    data = request.json
    payment_token = data.get('payment_token')
    
    # Procesar pago
    payment_response = requests.post(
        f"{PAYMENT_SERVICE}/process_payment",
        json={"payment_token": payment_token, "amount": 29.99, "description": "Premium upgrade"}
    )
    
    if payment_response.status_code != 200:
        return jsonify({"error": "Payment processing failed"}), 400
    
    # Actualizar usuario a premium
    user_id = request.user_info.get('user_id')
    upgrade_response = requests.post(
        f"{AUTH_SERVICE}/upgrade_user/{user_id}",
        json={"user_type": "premium"}
    )
    
    return jsonify(upgrade_response.json()), upgrade_response.status_code

# Añadir servicio individual
@app.route('/api/user/add_service', methods=['POST'])
@require_api_key
def add_service():
    data = request.json
    service_name = data.get('service_name')
    payment_token = data.get('payment_token')
    
    # Obtener precio del servicio
    price_response = requests.get(f"{PAYMENT_SERVICE}/service_price/{service_name}")
    if price_response.status_code != 200:
        return jsonify({"error": "Invalid service"}), 400
    
    price = price_response.json().get('price')
    
    # Procesar pago
    payment_response = requests.post(
        f"{PAYMENT_SERVICE}/process_payment",
        json={"payment_token": payment_token, "amount": price, "description": f"Service: {service_name}"}
    )
    
    if payment_response.status_code != 200:
        return jsonify({"error": "Payment processing failed"}), 400
    
    # Añadir servicio al usuario
    user_id = request.user_info.get('user_id')
    service_response = requests.post(
        f"{AUTH_SERVICE}/add_service/{user_id}",
        json={"service_name": service_name}
    )
    
    return jsonify(service_response.json()), service_response.status_code

# Listar servicios disponibles
@app.route('/api/available_services', methods=['GET'])
@require_api_key
def available_services():
    user_type = request.user_info.get('user_type')
    user_services = request.user_info.get('services', [])
    
    # Definir todos los servicios
    all_services = {
        "zodiac": {
            "description": "Información sobre tu signo zodiacal occidental y chino"
        },
        "music": {
            "description": "Canciones populares en tu fecha de nacimiento"
        },
        "astronomy": {
            "description": "Posiciones planetarias y fases lunares en tu fecha de nacimiento"
        },
        "weather": {
            "description": "Condiciones climáticas históricas en tu fecha de nacimiento"
        },
        "astro_report": {
            "description": "Análisis astrológico detallado"
        },
        "news": {
            "description": "Eventos históricos y mensajes especiales"
        },
        "compatibility": {
            "description": "Análisis de compatibilidad de pareja"
        },
        "location": {
            "description": "Lugares recomendados según tu carta astral"
        },
        "openai": {
            "description": "Interpretación avanzada con IA"
        }
    }
    
    # Marcar servicios disponibles según el tipo de usuario
    result = {"user_type": user_type, "services": {}}
    
    for service, info in all_services.items():
        if user_type == 'premium' or service in user_services or service == 'zodiac':
            info["available"] = True
        else:
            info["available"] = False
        result["services"][service] = info
    
    return jsonify(result), 200

# Generar reporte gratuito
@app.route('/api/generate_free_report', methods=['POST'])
@require_api_key
def generate_free_report():
    data = request.json
    name = data.get('name')
    date_of_birth = data.get('date_of_birth')
    time_of_birth = data.get('time_of_birth')
    city_of_birth = data.get('city_of_birth')
    language = data.get('language', 'es')  # Idioma por defecto: español
    
    if not all([name, date_of_birth, time_of_birth, city_of_birth]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Obtener información zodiacal
    zodiac_response = requests.post(
        f"{ZODIAC_SERVICE}/get_zodiac_info",
        json={"date_of_birth": date_of_birth, "language": language}
    )
    
    if zodiac_response.status_code != 200:
        return jsonify({"error": "Failed to get zodiac information"}), 500
    
    zodiac_info = zodiac_response.json()
    
    # Generar reporte básico
    report_data = {
        "name": name,
        "date_of_birth": date_of_birth,
        "time_of_birth": time_of_birth,
        "city_of_birth": city_of_birth,
        "language": language,
        "report_type": "free",
        "zodiac_info": zodiac_info
    }
    
    # Generar PDF
    pdf_response = requests.post(
        f"{PDF_SERVICE}/generate_pdf",
        json={"report_data": report_data, "report_type": "free", "language": language}
    )
    
    if pdf_response.status_code != 200:
        return jsonify({"error": "Failed to generate PDF"}), 500
    
    # Devolver el PDF como respuesta
    pdf_file = pdf_response.content
    return send_file(
        io.BytesIO(pdf_file),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"reporte_astral_{name.replace(' ', '_')}.pdf"
    )

# Generar reporte premium
@app.route('/api/generate_premium_report', methods=['POST'])
@require_api_key
def generate_premium_report():
    # Verificar si el usuario es premium o tiene acceso a los servicios solicitados
    user_type = request.user_info.get('user_type')
    user_services = request.user_info.get('services', [])
    
    data = request.json
    name = data.get('name')
    date_of_birth = data.get('date_of_birth')
    time_of_birth = data.get('time_of_birth')
    city_of_birth = data.get('city_of_birth')
    language = data.get('language', 'es')  # Idioma por defecto: español
    requested_services = data.get('services', [])
    
    if not all([name, date_of_birth, time_of_birth, city_of_birth]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Verificar acceso a los servicios solicitados
    if user_type != 'premium':
        for service in requested_services:
            if service not in user_services and service != 'zodiac':
                return jsonify({"error": f"Access to {service} service is not available with your account"}), 403
    
    # Inicializar datos del reporte
    report_data = {
        "name": name,
        "date_of_birth": date_of_birth,
        "time_of_birth": time_of_birth,
        "city_of_birth": city_of_birth,
        "language": language,
        "report_type": "premium"
    }
    
    # Obtener información zodiacal (siempre incluida)
    zodiac_response = requests.post(
        f"{ZODIAC_SERVICE}/get_zodiac_info",
        json={"date_of_birth": date_of_birth, "language": language}
    )
    
    if zodiac_response.status_code == 200:
        report_data["zodiac_info"] = zodiac_response.json()
    
    # Obtener información de servicios adicionales según lo solicitado
    service_endpoints = {
        "music": {"endpoint": f"{MUSIC_SERVICE}/get_music_info", "param": "date_of_birth"},
        "astronomy": {"endpoint": f"{ASTRONOMY_SERVICE}/get_astronomy_info", "param": "date_of_birth"},
        "weather": {"endpoint": f"{WEATHER_SERVICE}/get_weather_info", "param": "date_of_birth"},
        "astro_report": {"endpoint": f"{ASTRO_REPORT_SERVICE}/get_astro_report", "params": ["date_of_birth", "time_of_birth", "city_of_birth"]},
        "news": {"endpoint": f"{NEWS_SERVICE}/get_news", "param": "date_of_birth"},
        "openai": {"endpoint": f"{OPENAI_SERVICE}/get_ai_interpretation", "params": ["date_of_birth", "zodiac_info"]},
    }
    
    # Servicios especiales que requieren parámetros adicionales
    if "compatibility" in requested_services:
        partner_name = data.get('partner_name')
        partner_date = data.get('partner_date_of_birth')
        
        if partner_name and partner_date:
            compatibility_response = requests.post(
                f"{COMPATIBILITY_SERVICE}/get_compatibility",
                json={
                    "person1_date": date_of_birth,
                    "person2_date": partner_date,
                    "person1_name": name,
                    "person2_name": partner_name,
                    "language": language
                }
            )
            
            if compatibility_response.status_code == 200:
                report_data["compatibility_data"] = compatibility_response.json()
    
    if "location" in requested_services:
        location_response = requests.post(
            f"{LOCATION_SERVICE}/get_recommended_locations",
            json={
                "date_of_birth": date_of_birth,
                "time_of_birth": time_of_birth,
                "language": language
            }
        )
        
        if location_response.status_code == 200:
            report_data["location_data"] = location_response.json()
    
    # Procesar servicios estándar
    for service, info in service_endpoints.items():
        if service in requested_services:
            service_data = {}
            
            if "param" in info:
                service_data[info["param"]] = data.get(info["param"])
            elif "params" in info:
                for param in info["params"]:
                    if param in data:
                        service_data[param] = data.get(param)
                    elif param == "zodiac_info" and "zodiac_info" in report_data:
                        service_data[param] = report_data["zodiac_info"]
            
            # Añadir idioma a todos los servicios
            service_data["language"] = language
            
            service_response = requests.post(info["endpoint"], json=service_data)
            
            if service_response.status_code == 200:
                report_data[f"{service}_data"] = service_response.json()
    
    # Generar PDF
    pdf_response = requests.post(
        f"{PDF_SERVICE}/generate_pdf",
        json={"report_data": report_data, "report_type": "premium", "language": language}
    )
    
    if pdf_response.status_code != 200:
        return jsonify({"error": "Failed to generate PDF"}), 500
    
    pdf_file = pdf_response.content
    
    # Enviar por email si se solicita
    if "email" in requested_services and "email_address" in data:
        email_address = data.get("email_address")
        email_response = requests.post(
            f"{EMAIL_SERVICE}/send_email",
            json={
                "email": email_address,
                "subject": f"Tu reporte astrológico - {name}",
                "message": f"Hola {name},\n\nAdjunto encontrarás tu reporte astrológico personalizado.\n\nSaludos,\nEquipo Astrofuturo",
                "attachment": base64.b64encode(pdf_file).decode('utf-8'),
                "attachment_name": f"reporte_astral_{name.replace(' ', '_')}.pdf",
                "language": language
            }
        )
    
    # Enviar notificación por WhatsApp si se solicita
    if "whatsapp" in requested_services and "phone_number" in data:
        phone_number = data.get("phone_number")
        whatsapp_response = requests.post(
            f"{WHATSAPP_SERVICE}/send_message",
            json={
                "phone_number": phone_number,
                "message": f"Hola {name}, tu reporte astrológico está listo. Puedes acceder a él a través del enlace que te enviamos por correo electrónico.",
                "language": language
            }
        )
    
    # Devolver el PDF como respuesta
    return send_file(
        io.BytesIO(pdf_file),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"reporte_astral_{name.replace(' ', '_')}.pdf"
    )

# Listar precios de servicios
@app.route('/payment/services', methods=['GET'])
@require_api_key
def service_prices():
    response = requests.get(f"{PAYMENT_SERVICE}/services")
    return jsonify(response.json()), response.status_code

# Verificar estado de servicios
@app.route('/api/health', methods=['GET'])
def health_check():
    services = {
        "auth": AUTH_SERVICE,
        "zodiac": ZODIAC_SERVICE,
        "music": MUSIC_SERVICE,
        "astronomy": ASTRONOMY_SERVICE,
        "weather": WEATHER_SERVICE,
        "astro_report": ASTRO_REPORT_SERVICE,
        "news": NEWS_SERVICE,
        "pdf": PDF_SERVICE,
        "compatibility": COMPATIBILITY_SERVICE,
        "openai": OPENAI_SERVICE,
        "location": LOCATION_SERVICE,
        "email": EMAIL_SERVICE,
        "whatsapp": WHATSAPP_SERVICE,
        "payment": PAYMENT_SERVICE
    }
    
    results = {"status": "healthy", "services": {}}
    all_healthy = True
    
    for name, url in services.items():
        try:
            response = requests.get(f"{url}/health")
            if response.status_code == 200:
                results["services"][name] = {"status": "up", "code": 200}
            else:
                results["services"][name] = {"status": "degraded", "code": response.status_code}
                all_healthy = False
        except:
            results["services"][name] = {"status": "down", "code": 0}
            all_healthy = False
    
    if not all_healthy:
        results["status"] = "degraded"
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# Endpoints para el servicio de música
@app.route('/api/music/charts/<chart_name>', methods=['GET'])
@require_api_key
def get_music_chart(chart_name):
    date = request.args.get('date')
    params = {}
    if date:
        params['date'] = date
    response = requests.get("http://music_service:5002/charts/" + chart_name, params=params)
    return jsonify(response.json()), response.status_code

@app.route('/api/music/available_charts', methods=['GET'])
@require_api_key
def get_available_charts():
    response = requests.get("http://music_service:5002/available_charts")
    return jsonify(response.json()), response.status_code

@app.route('/api/music/search', methods=['GET'])
@require_api_key
def search_music():
    query = request.args.get('q')
    chart = request.args.get('chart')
    date = request.args.get('date')
    
    params = {'q': query}
    if chart:
        params['chart'] = chart
    if date:
        params['date'] = date
    
    response = requests.get("http://music_service:5002/search", params=params)
    return jsonify(response.json()), response.status_code

@app.route('/api/music/artist/<artist_name>', methods=['GET'])
@require_api_key
def get_artist_songs(artist_name):
    chart = request.args.get('chart')
    date = request.args.get('date')
    
    params = {}
    if chart:
        params['chart'] = chart
    if date:
        params['date'] = date
    
    response = requests.get("http://music_service:5002/artist/" + artist_name, params=params)
    return jsonify(response.json()), response.status_code


# Endpoints para el servicio de música
@app.route('/api/music/charts/<chart_name>', methods=['GET'])
@require_api_key
def get_music_chart(chart_name):
    date = request.args.get('date')
    params = {}
    if date:
        params['date'] = date
    response = requests.get("http://music_service:5002/charts/" + chart_name, params=params)
    return jsonify(response.json()), response.status_code

@app.route('/api/music/available_charts', methods=['GET'])
@require_api_key
def get_available_charts():
    response = requests.get("http://music_service:5002/available_charts")
    return jsonify(response.json()), response.status_code

@app.route('/api/music/search', methods=['GET'])
@require_api_key
def search_music():
    query = request.args.get('q')
    chart = request.args.get('chart')
    date = request.args.get('date')
    
    params = {'q': query}
    if chart:
        params['chart'] = chart
    if date:
        params['date'] = date
    
    response = requests.get("http://music_service:5002/search", params=params)
    return jsonify(response.json()), response.status_code

@app.route('/api/music/artist/<artist_name>', methods=['GET'])
@require_api_key
def get_artist_songs(artist_name):
    chart = request.args.get('chart')
    date = request.args.get('date')
    
    params = {}
    if chart:
        params['chart'] = chart
    if date:
        params['date'] = date
    
    response = requests.get("http://music_service:5002/artist/" + artist_name, params=params)
    return jsonify(response.json()), response.status_code


# Endpoint de prueba
@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "API Gateway funcionando correctamente"}), 200


# Definición del servicio de películas
MOVIE_SERVICE = "http://movie_service:5000"

# Rutas para el servicio de películas
@app.route('/api/movies/discover', methods=['GET'])
@require_api_key
def movie_discover():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/discover", request)

@app.route('/api/movies/between_dates', methods=['GET'])
@require_api_key
def movie_between_dates():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/between_dates", request)

@app.route('/api/movies/search', methods=['GET'])
@require_api_key
def movie_search():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/search", request)

@app.route('/api/movies/genres', methods=['GET'])
@require_api_key
def movie_genres():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/genres", request)

@app.route('/api/movies/by_genre/<int:genre_id>', methods=['GET'])
@require_api_key
def movie_by_genre(genre_id):
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/by_genre/{genre_id}", request)

@app.route('/api/movies/details/<int:movie_id>', methods=['GET'])
@require_api_key
def movie_details_proxy(movie_id):
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/details/{movie_id}", request)

@app.route('/api/movies/now_playing', methods=['GET'])
@require_api_key
def movie_now_playing():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/now_playing", request)

@app.route('/api/movies/top_rated', methods=['GET'])
@require_api_key
def movie_top_rated():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/top_rated", request)

# Definición del servicio de películas
MOVIE_SERVICE = "http://movie_service:5000"

# Rutas para el servicio de películas
@app.route('/api/movies/discover', methods=['GET'])
@require_api_key
def movie_discover():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/discover", request)

@app.route('/api/movies/between_dates', methods=['GET'])
@require_api_key
def movie_between_dates():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/between_dates", request)

@app.route('/api/movies/search', methods=['GET'])
@require_api_key
def movie_search():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/search", request)

@app.route('/api/movies/genres', methods=['GET'])
@require_api_key
def movie_genres():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/genres", request)

@app.route('/api/movies/by_genre/<int:genre_id>', methods=['GET'])
@require_api_key
def movie_by_genre(genre_id):
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/by_genre/{genre_id}", request)

@app.route('/api/movies/details/<int:movie_id>', methods=['GET'])
@require_api_key
def movie_details_proxy(movie_id):
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/details/{movie_id}", request)

@app.route('/api/movies/now_playing', methods=['GET'])
@require_api_key
def movie_now_playing():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/now_playing", request)

@app.route('/api/movies/top_rated', methods=['GET'])
@require_api_key
def movie_top_rated():
    return proxy_request(f"{MOVIE_SERVICE}/api/movies/top_rated", request)
