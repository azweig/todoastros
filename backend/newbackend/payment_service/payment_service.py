from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import logging
import requests
import os
import json
import sqlite3
import hashlib
from datetime import datetime
import stripe
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("payment_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("payment_service")

app = Flask(__name__)
CORS(app)

# URLs de los servicios
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://auth_service:5050")

# Configuración de Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
SUCCESS_URL = os.environ.get("SUCCESS_URL", "http://localhost:3000/payment/success")
CANCEL_URL = os.environ.get("CANCEL_URL", "http://localhost:3000/payment/cancel")

# Configuración de la base de datos
DB_PATH = "/data/payment_transactions.db"

def init_db():
    """Inicializa la base de datos."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla para almacenar transacciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        stripe_session_id TEXT UNIQUE NOT NULL,
        amount REAL NOT NULL,
        currency TEXT NOT NULL,
        status TEXT NOT NULL,
        product_type TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')

    # Crear tabla para almacenar suscripciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        stripe_subscription_id TEXT UNIQUE NOT NULL,
        status TEXT NOT NULL,
        current_period_start TEXT NOT NULL,
        current_period_end TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    logger.info("Base de datos inicializada")

# Inicializar la base de datos al arrancar
init_db()

def verify_api_key(api_key):
    """Verifica la API key con el servicio de autenticación."""
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/verify",
            json={"api_key": api_key}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Error al verificar API key: {str(e)}")
        return None

def update_user_subscription(user_id, subscription_end_date):
    """Actualiza la fecha de fin de suscripción del usuario."""
    try:
        # Aquí deberíamos tener un endpoint en el servicio de autenticación para actualizar la suscripción
        # Por ahora, lo simulamos con un log
        logger.info(f"Actualizando suscripción para usuario {user_id} hasta {subscription_end_date}")
        return True
    except Exception as e:
        logger.error(f"Error al actualizar suscripción: {str(e)}")
        return False

def store_transaction(user_id, session_id, amount, currency, status, product_type):
    """Almacena una transacción en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    try:
        cursor.execute(
            "INSERT INTO transactions (user_id, stripe_session_id, amount, currency, status, product_type, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, session_id, amount, currency, status, product_type, now, now)
        )
        conn.commit()
        logger.info(f"Transacción almacenada: {session_id}")
        return True
    except Exception as e:
        logger.error(f"Error al almacenar transacción: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_transaction_status(session_id, status):
    """Actualiza el estado de una transacción."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    try:
        cursor.execute(
            "UPDATE transactions SET status = ?, updated_at = ? WHERE stripe_session_id = ?",
            (status, now, session_id)
        )
        conn.commit()
        logger.info(f"Estado de transacción actualizado: {session_id} -> {status}")
        return True
    except Exception as e:
        logger.error(f"Error al actualizar estado de transacción: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def store_subscription(user_id, subscription_id, status, period_start, period_end):
    """Almacena una suscripción en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    try:
        cursor.execute(
            "INSERT INTO subscriptions (user_id, stripe_subscription_id, status, current_period_start, current_period_end, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, subscription_id, status, period_start, period_end, now, now)
        )
        conn.commit()
        logger.info(f"Suscripción almacenada: {subscription_id}")
        return True
    except Exception as e:
        logger.error(f"Error al almacenar suscripción: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_subscription_status(subscription_id, status, period_start=None, period_end=None):
    """Actualiza el estado de una suscripción."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    try:
        if period_start and period_end:
            cursor.execute(
                "UPDATE subscriptions SET status = ?, current_period_start = ?, current_period_end = ?, updated_at = ? WHERE stripe_subscription_id = ?",
                (status, period_start, period_end, now, subscription_id)
            )
        else:
            cursor.execute(
                "UPDATE subscriptions SET status = ?, updated_at = ? WHERE stripe_subscription_id = ?",
                (status, now, subscription_id)
            )
        conn.commit()
        logger.info(f"Estado de suscripción actualizado: {subscription_id} -> {status}")
        return True
    except Exception as e:
        logger.error(f"Error al actualizar estado de suscripción: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar la salud del servicio."""
    return jsonify({"status": "up"}), 200

@app.route('/payment/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Crea una sesión de pago con Stripe."""
    try:
        # Verificar API key
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401
        
        user_info = verify_api_key(api_key)
        if not user_info or not user_info.get("valid"):
            return jsonify({"error": "Invalid API key"}), 401
        
        user_id = user_info.get("user_id")
        
        # Obtener datos de la solicitud
        data = request.get_json()
        product_type = data.get('product_type', 'premium_monthly')
        quantity = data.get('quantity', 1)
        
        # Configurar los detalles del producto según el tipo
        products = {
            'premium_monthly': {
                'name': 'Suscripción Premium Mensual',
                'description': 'Acceso a todas las funciones premium por un mes',
                'amount': 999,  # $9.99
                'currency': 'usd',
                'interval': 'month'
            },
            'premium_yearly': {
                'name': 'Suscripción Premium Anual',
                'description': 'Acceso a todas las funciones premium por un año',
                'amount': 9999,  # $99.99
                'currency': 'usd',
                'interval': 'year'
            },
            'single_report': {
                'name': 'Informe Astrológico Individual',
                'description': 'Un informe astrológico detallado personalizado',
                'amount': 1999,  # $19.99
                'currency': 'usd',
                'is_subscription': False
            }
        }
        
        if product_type not in products:
            return jsonify({"error": "Invalid product type"}), 400
        
        product = products[product_type]
        is_subscription = product.get('is_subscription', True)
        
        # Crear sesión de pago
        if is_subscription:
            # Crear un producto y un precio para la suscripción
            stripe_product = stripe.Product.create(
                name=product['name'],
                description=product['description']
            )
            
            stripe_price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=product['amount'],
                currency=product['currency'],
                recurring={"interval": product['interval']}
            )
            
            # Crear sesión de pago para suscripción
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': stripe_price.id,
                    'quantity': quantity,
                }],
                mode='subscription',
                success_url=SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=CANCEL_URL,
                client_reference_id=str(user_id)
            )
        else:
            # Crear sesión de pago para producto único
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': product['currency'],
                        'product_data': {
                            'name': product['name'],
                            'description': product['description'],
                        },
                        'unit_amount': product['amount'],
                    },
                    'quantity': quantity,
                }],
                mode='payment',
                success_url=SUCCESS_URL + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=CANCEL_URL,
                client_reference_id=str(user_id)
            )
        
        # Almacenar la transacción en la base de datos
        store_transaction(
            user_id=user_id,
            session_id=checkout_session.id,
            amount=product['amount'] * quantity / 100,  # Convertir a dólares
            currency=product['currency'],
            status='pending',
            product_type=product_type
        )
        
        return jsonify({
            'id': checkout_session.id,
            'url': checkout_session.url
        })
        
    except Exception as e:
        logger.error(f"Error al crear sesión de pago: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/payment/webhook', methods=['POST'])
def webhook():
    """Maneja los webhooks de Stripe."""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f"Payload inválido: {str(e)}")
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Firma inválida: {str(e)}")
        return jsonify({"error": "Invalid signature"}), 400
    
    # Manejar el evento
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Obtener el ID de usuario desde la referencia del cliente
        user_id = int(session.get('client_reference_id', 0))
        if not user_id:
            logger.error("No se pudo obtener el ID de usuario")
            return jsonify({"error": "User ID not found"}), 400
        
        # Actualizar el estado de la transacción
        update_transaction_status(session.id, 'completed')
        
        # Si es una suscripción, almacenar los detalles
        if session.get('mode') == 'subscription':
            subscription_id = session.get('subscription')
            if subscription_id:
                # Obtener detalles de la suscripción
                subscription = stripe.Subscription.retrieve(subscription_id)
                
                # Calcular fechas de período
                period_start = datetime.fromtimestamp(subscription.current_period_start).isoformat()
                period_end = datetime.fromtimestamp(subscription.current_period_end).isoformat()
                
                # Almacenar la suscripción
                store_subscription(
                    user_id=user_id,
                    subscription_id=subscription_id,
                    status=subscription.status,
                    period_start=period_start,
                    period_end=period_end
                )
                
                # Actualizar la fecha de fin de suscripción del usuario
                update_user_subscription(user_id, period_end)
    
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        subscription_id = invoice.get('subscription')
        
        if subscription_id:
            # Obtener detalles de la suscripción
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            # Calcular fechas de período
            period_start = datetime.fromtimestamp(subscription.current_period_start).isoformat()
            period_end = datetime.fromtimestamp(subscription.current_period_end).isoformat()
            
            # Actualizar el estado de la suscripción
            update_subscription_status(
                subscription_id=subscription_id,
                status=subscription.status,
                period_start=period_start,
                period_end=period_end
            )
            
            # Obtener el ID de usuario desde la suscripción
            # Esto requiere que hayamos almacenado el user_id en la tabla de suscripciones
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM subscriptions WHERE stripe_subscription_id = ?", (subscription_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                user_id = result[0]
                # Actualizar la fecha de fin de suscripción del usuario
                update_user_subscription(user_id, period_end)
    
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        subscription_id = subscription.get('id')
        
        if subscription_id:
            # Calcular fechas de período
            period_start = datetime.fromtimestamp(subscription.current_period_start).isoformat()
            period_end = datetime.fromtimestamp(subscription.current_period_end).isoformat()
            
            # Actualizar el estado de la suscripción
            update_subscription_status(
                subscription_id=subscription_id,
                status=subscription.status,
                period_start=period_start,
                period_end=period_end
            )
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        subscription_id = subscription.get('id')
        
        if subscription_id:
            # Actualizar el estado de la suscripción
            update_subscription_status(
                subscription_id=subscription_id,
                status='canceled'
            )
    
    return jsonify({"success": True})

@app.route('/payment/customer-portal', methods=['POST'])
def customer_portal():
    """Crea una sesión del portal de clientes de Stripe."""
    try:
        # Verificar API key
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401
        
        user_info = verify_api_key(api_key)
        if not user_info or not user_info.get("valid"):
            return jsonify({"error": "Invalid API key"}), 401
        
        data = request.get_json()
        customer_id = data.get('customer_id')
        
        if not customer_id:
            return jsonify({"error": "Customer ID is required"}), 400
        
        # Crear sesión del portal
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=data.get('return_url', 'http://localhost:3000/account')
        )
        
        return jsonify({
            'url': session.url
        })
        
    except Exception as e:
        logger.error(f"Error al crear sesión del portal: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/payment/subscription-status', methods=['GET'])
def subscription_status():
    """Obtiene el estado de la suscripción de un usuario."""
    try:
        # Verificar API key
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401
        
        user_info = verify_api_key(api_key)
        if not user_info or not user_info.get("valid"):
            return jsonify({"error": "Invalid API key"}), 401
        
        user_id = user_info.get("user_id")
        
        # Obtener la suscripción más reciente del usuario
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT stripe_subscription_id, status, current_period_start, current_period_end FROM subscriptions WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return jsonify({
                "has_subscription": False,
                "message": "No active subscription found"
            })
        
        subscription_id, status, period_start, period_end = result
        
        # Verificar si la suscripción está activa
        is_active = status == 'active'
        
        return jsonify({
            "has_subscription": is_active,
            "subscription_id": subscription_id,
            "status": status,
            "current_period_start": period_start,
            "current_period_end": period_end
        })
        
    except Exception as e:
        logger.error(f"Error al obtener estado de suscripción: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/payment/transactions', methods=['GET'])
def get_transactions():
    """Obtiene las transacciones de un usuario."""
    try:
        # Verificar API key
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key is required"}), 401
        
        user_info = verify_api_key(api_key)
        if not user_info or not user_info.get("valid"):
            return jsonify({"error": "Invalid API key"}), 401
        
        user_id = user_info.get("user_id")
        
        # Obtener las transacciones del usuario
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT stripe_session_id, amount, currency, status, product_type, created_at FROM transactions WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        transactions = []
        for row in cursor.fetchall():
            session_id, amount, currency, status, product_type, created_at = row
            transactions.append({
                "session_id": session_id,
                "amount": amount,
                "currency": currency,
                "status": status,
                "product_type": product_type,
                "created_at": created_at
            })
        conn.close()
        
        return jsonify({
            "transactions": transactions
        })
        
    except Exception as e:
        logger.error(f"Error al obtener transacciones: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5014)
