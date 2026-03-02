from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
import os
import requests
import sqlite3
import base64
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("email_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("email_service")

app = Flask(__name__)

# URL del servicio de autenticación
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://localhost:5050")

# Configuración de email
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USER = os.environ.get("EMAIL_USER", "tu_email@gmail.com")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "tu_contraseña")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "Astrofuturo <noreply@astrofuturo.com>")

def verify_api_key(api_key):
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/verify",
            json={"api_key": api_key}
        )
        return response.status_code == 200 and response.json().get("valid", False)
    except Exception as e:
        logger.error(f"Error al verificar API key: {str(e)}")
        return False

def init_db():
    conn = sqlite3.connect('email.db')
    cursor = conn.cursor()
    
    # Tabla para registro de emails enviados
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        to_email TEXT NOT NULL,
        subject TEXT NOT NULL,
        has_attachment BOOLEAN NOT NULL DEFAULT 0,
        status TEXT NOT NULL,
        error_message TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def send_email(to_email, subject, body, attachment=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Añadir adjunto si existe
        if attachment:
            # Decodificar el adjunto si está en base64
            try:
                attachment_data = base64.b64decode(attachment)
            except:
                # Si no es base64, usar directamente
                attachment_data = attachment.encode('latin1')
            
            part = MIMEApplication(attachment_data)
            part.add_header('Content-Disposition', 'attachment', filename=f"reporte_{datetime.now().strftime('%Y%m%d')}.pdf")
            msg.attach(part)
        
        # Conectar al servidor SMTP
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        
        # Enviar email
        server.send_message(msg)
        server.quit()
        
        return True, "Email enviado exitosamente"
    except Exception as e:
        logger.error(f"Error al enviar email: {str(e)}")
        return False, str(e)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/email', methods=['POST'])
def email():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        logger.warning(f"Intento de acceso con API key inválida: {api_key}")
        return jsonify({"error": "API key inválida o faltante"}), 401
    
    data = request.get_json()
    to_email = data.get('to')
    subject = data.get('subject')
    body = data.get('body')
    attachment = data.get('attachment')

    if not all([to_email, subject, body]):
        logger.warning("Solicitud sin datos obligatorios")
        return jsonify({"error": "Faltan datos obligatorios: to, subject, body"}), 400

    try:
        # Enviar email
        success, message = send_email(to_  subject, body"}), 400

    try:
        # Enviar email
        success, message = send_email(to_email, subject, body, attachment)
        
        # Registrar en la base de datos
        conn = sqlite3.connect('email.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO email_log (to_email, subject, has_attachment, status, error_message) VALUES (?, ?, ?, ?, ?)",
            (to_email, subject, 1 if attachment else 0, "success" if success else "error", None if success else message)
        )
        conn.commit()
        conn.close()
        
        if success:
            logger.info(f"Email enviado exitosamente a {to_email}")
            return jsonify({"message": "Email enviado exitosamente"}), 200
        else:
            logger.error(f"Error al enviar email a {to_email}: {message}")
            return jsonify({"error": f"Error al enviar email: {message}"}), 500
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5012)

