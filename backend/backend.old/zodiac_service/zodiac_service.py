from flask import Flask, request, jsonify
import sqlite3
import logging
import requests
import os
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("zodiac_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("zodiac_service")

app = Flask(__name__)

# URL del servicio de autenticación
AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://localhost:5050")

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect('zodiac.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS zodiac_cache (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_of_birth TEXT UNIQUE NOT NULL,
        western_zodiac TEXT NOT NULL,
        chinese_zodiac TEXT NOT NULL,
        vedic_zodiac TEXT NOT NULL,
        mayan_zodiac TEXT NOT NULL,
        egyptian_zodiac TEXT NOT NULL,
        celtic_zodiac TEXT NOT NULL,
        draconic_zodiac TEXT NOT NULL,
        native_american_zodiac TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

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

def get_zodiac_sign(date_of_birth):
    """Determina el signo zodiacal occidental basado en la fecha de nacimiento."""
    try:
        month, day = map(int, date_of_birth.split("-")[1:])

        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Tauro"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Géminis"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cáncer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Escorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagitario"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricornio"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Acuario"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "Piscis"
        return "Desconocido"
    except Exception as e:
        logger.error(f"Error al determinar signo zodiacal occidental: {str(e)}")
        return "Error"

def get_chinese_zodiac(date_of_birth):
    """Determina el signo zodiacal chino basado en el año de nacimiento."""
    try:
        year = int(date_of_birth.split("-")[0])
        animals = [
            "Rata", "Buey", "Tigre", "Conejo", "Dragón", "Serpiente",
            "Caballo", "Cabra", "Mono", "Gallo", "Perro", "Cerdo"
        ]
        return animals[(year - 4) % 12]
    except Exception as e:
        logger.error(f"Error al determinar signo zodiacal chino: {str(e)}")
        return "Error"

def get_vedic_zodiac(date_of_birth):
    """Determina el signo zodiacal védico (sideral) basado en la fecha de nacimiento."""
    try:
        # El zodíaco védico está desplazado aproximadamente 23 grados del zodíaco occidental
        # Esta es una simplificación, en la realidad se necesitaría un cálculo astronómico más preciso
        month, day = map(int, date_of_birth.split("-")[1:])
        
        # Desplazamiento aproximado de 23 días
        if (month == 4 and day >= 14) or (month == 5 and day <= 14):
            return "Mesha (Aries)"
        elif (month == 5 and day >= 15) or (month == 6 and day <= 14):
            return "Vrishabha (Tauro)"
        elif (month == 6 and day >= 15) or (month == 7 and day <= 14):
            return "Mithuna (Géminis)"
        elif (month == 7 and day >= 15) or (month == 8 and day <= 14):
            return "Karka (Cáncer)"
        elif (month == 8 and day >= 15) or (month == 9 and day <= 14):
            return "Simha (Leo)"
        elif (month == 9 and day >= 15) or (month == 10 and day <= 14):
            return "Kanya (Virgo)"
        elif (month == 10 and day >= 15) or (month == 11 and day <= 14):
            return "Tula (Libra)"
        elif (month == 11 and day >= 15) or (month == 12 and day <= 14):
            return "Vrishchika (Escorpio)"
        elif (month == 12 and day >= 15) or (month == 1 and day <= 13):
            return "Dhanu (Sagitario)"
        elif (month == 1 and day >= 14) or (month == 2 and day <= 12):
            return "Makara (Capricornio)"
        elif (month == 2 and day >= 13) or (month == 3 and day <= 14):
            return "Kumbha (Acuario)"
        elif (month == 3 and day >= 15) or (month == 4 and day <= 13):
            return "Meena (Piscis)"
        return "Desconocido"
    except Exception as e:
        logger.error(f"Error al determinar signo zodiacal védico: {str(e)}")
        return "Error"

def get_mayan_zodiac(date_of_birth):
    """Determina el signo zodiacal maya basado en la fecha de nacimiento."""
    try:
        month, day = map(int, date_of_birth.split("-")[1:])
        
        if (month == 12 and day >= 13) or (month == 1 and day <= 9):
            return "Murciélago"
        elif (month == 1 and day >= 10) or (month == 2 and day <= 6):
            return "Escorpión"
        elif (month == 2 and day >= 7) or (month == 3 and day <= 6):
            return "Venado"
        elif (month == 3 and day >= 7) or (month == 4 and day <= 3):
            return "Búho"
        elif (month == 4 and day >= 4) or (month == 5 and day <= 1):
            return "Pavo Real"
        elif (month == 5 and day >= 2) or (month == 5 and day <= 29):
            return "Lagarto"
        elif (month == 5 and day >= 30) or (month == 6 and day <= 26):
            return "Mono"
        elif (month == 6 and day >= 27) or (month == 7 and day <= 25):
            return "Halcón"
        elif (month == 7 and day >= 26) or (month == 8 and day <= 22):
            return "Jaguar"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 19):
            return "Zorro"
        elif (month == 9 and day >= 20) or (month == 10 and day <= 17):
            return "Serpiente"
        elif (month == 10 and day >= 18) or (month == 11 and day <= 14):
            return "Ardilla"
        elif (month == 11 and day >= 15) or (month == 12 and day <= 12):
            return "Tortuga"
        return "Desconocido"
    except Exception as e:
        logger.error(f"Error al determinar signo zodiacal maya: {str(e)}")
        return "Error"

def get_egyptian_zodiac(date_of_birth):
    """Determina el signo zodiacal egipcio basado en la fecha de nacimiento."""
    try:
        month, day = map(int, date_of_birth.split("-")[1:])
        
        if (month == 1 and day >= 1) or (month == 1 and day <= 7):
            return "Nilo"
        elif (month == 1 and day >= 8) or (month == 1 and day <= 21):
            return "Amón-Ra"
        elif (month == 1 and day >= 22) or (month == 2 and day <= 4):
            return "Mut"
        elif (month == 2 and day >= 5) or (month == 2 and day <= 28):
            return "Geb"
        elif (month == 3 and day >= 1) or (month == 3 and day <= 10):
            return "Osiris"
        elif (month == 3 and day >= 11) or (month == 3 and day <= 31):
            return "Isis"
        elif (month == 4 and day >= 1) or (month == 4 and day <= 19):
            return "Thoth"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 7):
            return "Horus"
        elif (month == 5 and day >= 8) or (month == 5 and day <= 27):
            return "Anubis"
        elif (month == 5 and day >= 28) or (month == 6 and day <= 18):
            return "Seth"
        elif (month == 6 and day >= 19) or (month == 7 and day <= 13):
            return "Bastet"
        elif (month == 7 and day >= 14) or (month == 8 and day <= 8):
            return "Sekhmet"
        elif (month == 8 and day >= 9) or (month == 9 and day <= 2):
            return "Hathor"
        elif (month == 9 and day >= 3) or (month == 9 and day <= 28):
            return "Ptah"
        elif (month == 9 and day >= 29) or (month == 10 and day <= 30):
            return "Atum"
        elif (month == 10 and day >= 31) or (month == 11 and day <= 26):
            return "Hapi"
        elif (month == 11 and day >= 27) or (month == 12 and day <= 26):
            return "Maat"
        elif (month == 12 and day >= 27) or (month == 12 and day <= 31):
            return "Nilo"
        return "Desconocido"
    except Exception as e:
        logger.error(f"Error al determinar signo zodiacal egipcio: {str(e)}")
        return "Error"

def get_celtic_zodiac(date_of_birth):
    """Determina el signo zodiacal celta basado en la fecha de nacimiento."""
    try:
        month, day = map(int, date_of_birth.split("-")[1:])
        
        if (month == 12 and day >= 24) or (month == 1 and day <= 20):
            return "Abeto"
        elif (month == 1 and day >= 21) or (month == 2 and day <= 17):
            return "Olmo"
        elif (month == 2 and day >= 18) or (month == 3 and day <= 17):
            return "Ciprés"
        elif (month == 3 and day >= 18) or (month == 4 and day <= 14):
            return "Álamo"
        elif (month == 4 and day >= 15) or (month == 5 and day <= 12):
            return "Cedro"
        elif (month == 5 and day >= 13) or (month == 6 and day <= 9):
            return "Haya"
        elif (month == 6 and day >= 10) or (month == 7 and day <= 7):
            return "Manzano"
        elif (month == 7 and day >= 8) or (month == 8 and day <= 4):
            return "Abeto"
        elif (month == 8 and day >= 5) or (month == 9 and day <= 1):
            return "Sauce"
        elif (month == 9 and day >= 2) or (month == 9 and day <= 29):
            return "Avellano"
        elif (month == 9 and day >= 30) or (month == 10 and day <= 27):
            return "Serbal"
        elif (month == 10 and day >= 28) or (month == 11 and day <= 24):
            return "Olmo"
        elif (month == 11 and day >= 25) or (month == 12 and day <= 23):
            return "Saúco"
        return "Desconocido"
    except Exception as e:
        logger.error(f"Error al determinar signo zodiacal celta: {str(e)}")
        return "Error"

def get_draconic_zodiac(date_of_birth):
    """Determina el signo zodiacal dracónico basado en la fecha de nacimiento."""
    try:
        # El zodíaco dracónico se basa en la posición del nodo lunar norte
        # Esta es una simplificación, en la realidad se necesitaría un cálculo astronómico más preciso
        # Usaremos una aproximación basada en ciclos de 18.6 años
        year, month, day = map(int, date_of_birth.split("-"))
        
        # Calcular días transcurridos desde una fecha de referencia
        birth_date = datetime(year, month, day)
        reference_date = datetime(2000, 1, 1)  # Nodo norte en 0° de Aries
        days_diff = (birth_date - reference_date).days
        
        # El ciclo completo del nodo lunar es de aproximadamente 6798 días (18.6 años)
        position_in_cycle = (days_diff % 6798) / 6798 * 360  # Posición en grados
        
        # Determinar el signo basado en la posición
        if 0 <= position_in_cycle < 30:
            return "Aries Dracónico"
        elif 30 <= position_in_cycle < 60:
            return "Tauro Dracónico"
        elif 60 <= position_in_cycle < 90:
            return "Géminis Dracónico"
        elif 90 <= position_in_cycle < 120:
            return "Cáncer Dracónico"
        elif 120 <= position_in_cycle < 150:
            return "Leo Dracónico"
        elif 150 <= position_in_cycle < 180:
            return "Virgo Dracónico"
        elif 180 <= position_in_cycle < 210:
            return "Libra Dracónico"
        elif 210 <= position_in_cycle < 240:
            return "Escorpio Dracónico"
        elif 240 <= position_in_cycle < 270:
            return "Sagitario Dracónico"
        elif 270 <= position_in_cycle < 300:
            return "Capricornio Dracónico"
        elif 300 <= position_in_cycle < 330:
            return "Acuario Dracónico"
        elif 330 <= position_in_cycle < 360:
            return "Piscis Dracónico"
        return "Desconocido"
    except Exception as e:
        logger.error(f"Error al determinar signo zodiacal dracónico: {str(e)}")
        return "Error"

def get_native_american_zodiac(date_of_birth):
    """Determina el signo zodiacal nativo americano basado en la fecha de nacimiento."""
    try:
        month, day = map(int, date_of_birth.split("-")[1:])
        
        if (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Nutria"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "Lobo"
        elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Halcón"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Castor"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Ciervo"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 21):
            return "Pájaro Carpintero"
        elif (month == 7 and day >= 22) or (month == 8 and day <= 21):
            return "Salmón"
        elif (month == 8 and day >= 22) or (month == 9 and day <= 21):
            return "Oso Pardo"
        elif (month == 9 and day >= 22) or (month == 10 and day <= 22):
            return "Cuervo"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 22):
            return "Serpiente"
        elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
            return "Búho"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Ganso"
        return "Desconocido"
    except Exception as e:
        logger.error(f"Error al determinar signo zodiacal nativo americano: {str(e)}")
        return "Error"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/zodiac', methods=['POST'])
def zodiac():
    # Verificar API key
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        logger.warning(f"Intento de acceso con API key inválida: {api_key}")
        return jsonify({"error": "API key inválida o faltante"}), 401

    data = request.get_json()
    date_of_birth = data.get('date_of_birth')

    if not date_of_birth:
        logger.warning("Solicitud sin fecha de nacimiento")
        return jsonify({"error": "Falta la fecha de nacimiento"}), 400

    try:
        # Verificar si ya existe en caché
        conn = sqlite3.connect('zodiac.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT western_zodiac, chinese_zodiac, vedic_zodiac, mayan_zodiac, egyptian_zodiac, celtic_zodiac, draconic_zodiac, native_american_zodiac FROM zodiac_cache WHERE date_of_birth = ?",
            (date_of_birth,)
        )
        cached = cursor.fetchone()

        if cached:
            western_zodiac, chinese_zodiac, vedic_zodiac, mayan_zodiac, egyptian_zodiac, celtic_zodiac, draconic_zodiac, native_american_zodiac = cached
            logger.info(f"Datos zodiacales recuperados de caché para {date_of_birth}")
        else:
            western_zodiac = get_zodiac_sign(date_of_birth)
            chinese_zodiac = get_chinese_zodiac(date_of_birth)
            vedic_zodiac = get_vedic_zodiac(date_of_birth)
            mayan_zodiac = get_mayan_zodiac(date_of_birth)
            egyptian_zodiac = get_egyptian_zodiac(date_of_birth)
            celtic_zodiac = get_celtic_zodiac(date_of_birth)
            draconic_zodiac = get_draconic_zodiac(date_of_birth)
            native_american_zodiac = get_native_american_zodiac(date_of_birth)

            # Guardar en caché
            cursor.execute(
                "INSERT INTO zodiac_cache (date_of_birth, western_zodiac, chinese_zodiac, vedic_zodiac, mayan_zodiac, egyptian_zodiac, celtic_zodiac, draconic_zodiac, native_american_zodiac) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (date_of_birth, western_zodiac, chinese_zodiac, vedic_zodiac, mayan_zodiac, egyptian_zodiac, celtic_zodiac, draconic_zodiac, native_american_zodiac)
            )
            conn.commit()
            logger.info(f"Nuevos datos zodiacales calculados y guardados para {date_of_birth}")

        conn.close()

        return jsonify({
            "western_zodiac": western_zodiac,
            "chinese_zodiac": chinese_zodiac,
            "vedic_zodiac": vedic_zodiac,
            "mayan_zodiac": mayan_zodiac,
            "egyptian_zodiac": egyptian_zodiac,
            "celtic_zodiac": celtic_zodiac,
            "draconic_zodiac": draconic_zodiac,
            "native_american_zodiac": native_american_zodiac
        })

    except Exception as e:
        logger.error(f"Error al procesar solicitud zodiacal: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5001)
