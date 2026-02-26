import requests
import json
import random
import string
import time

# URL base de la API
BASE_URL = "https://api.todoastros.com"

# Función para generar contraseñas aleatorias
def generate_password(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for i in range(length))

# Función para procesar la ubicación de nacimiento
def process_birth_location(location_str):
    # Simplemente dividimos por coma y asumimos que el formato es "Ciudad, País"
    parts = location_str.split(',')
    city = parts[0].strip()
    country = parts[1].strip() if len(parts) > 1 else ""
    return city, country

# Función para extraer fecha y hora de nacimiento
def process_birth_datetime(date_str, time_str=None):
    # Asumimos que date_str está en formato "YYYY-MM-DD"
    if time_str:
        return date_str, time_str
    else:
        return date_str, "12:00"  # Hora por defecto si no se proporciona

def test_complete_flow():
    print("\n=== INICIANDO PRUEBA DE FLUJO COMPLETO ===\n")

    # Paso 1: Usuario elige entre carta astral gratuita o paga
    is_premium = input("¿Desea una carta astral premium? (s/n): ").lower() == 's'

    # Paso 2: Usuario ingresa sus datos
    full_name = input("Nombre completo: ")
    birth_date = input("Fecha de nacimiento (YYYY-MM-DD): ")
    birth_time = input("Hora de nacimiento (HH:MM, opcional - presione Enter para omitir): ") or None
    birth_location = input("Lugar de nacimiento (Ciudad, País): ")
    email = input("Correo electrónico: ")

    # Procesamos los datos ingresados
    first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, "")
    birth_date, birth_time = process_birth_datetime(birth_date, birth_time)
    birth_city, birth_country = process_birth_location(birth_location)

    # Generamos un nombre de usuario y contraseña
    username = email.split('@')[0] + str(random.randint(100, 999))
    password = generate_password()

    print(f"\nGenerando usuario: {username}")
    print(f"Contraseña: {password}")

    # Paso 3: Si es premium, procesamos el pago
    if is_premium:
        print("\n=== PROCESANDO PAGO ===")
        
        # Primero, registramos un usuario administrador para obtener una API key válida
        admin_username = f"admin_test_{random.randint(1000, 9999)}"
        admin_password = generate_password()
        
        admin_register_data = {
            "username": admin_username,
            "password": admin_password,
            "user_type": "admin",
            "admin_key": "astrofuturo_admin_key"
        }
        
        try:
            print(f"Registrando usuario administrador temporal: {admin_username}")
            admin_response = requests.post(
                f"{BASE_URL}/auth/register",
                json=admin_register_data
            )
            
            if admin_response.status_code == 201:
                admin_info = admin_response.json()
                api_key = admin_info.get("api_key")
                print(f"Usuario administrador registrado para pruebas")
            else:
                print(f"Error al registrar usuario administrador: {admin_response.status_code}")
                print(admin_response.text)
                return
        except Exception as e:
            print(f"Error en la solicitud de registro de administrador: {str(e)}")
            return
        
        # Ahora usamos la API key obtenida para el proceso de pago
        payment_data = {
            "product_type": "premium_monthly",
            "quantity": 1
        }

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": api_key
        }

        try:
            print(f"Enviando solicitud de pago con API key: {api_key}")
            response = requests.post(
                f"{BASE_URL}/api/payment/create-checkout-session",
                headers=headers,
                json=payment_data
            )

            if response.status_code == 200:
                payment_info = response.json()
                print(f"Pago procesado correctamente")
                print(f"URL de checkout: {payment_info['url']}")
                print("En un caso real, el usuario sería redirigido a esta URL")

                # Simulamos que el pago fue completado
                print("Simulando pago completado...")
                time.sleep(2)
            else:
                print(f"Error al procesar el pago: {response.status_code}")
                print(response.text)
                return
        except Exception as e:
            print(f"Error en la solicitud de pago: {str(e)}")
            return

    # Paso 4: Registramos al usuario
    print("\n=== REGISTRANDO USUARIO ===")

    register_data = {
        "username": username,
        "password": password,
        "user_type": "premium" if is_premium else "free"
    }

    # Si es premium, agregamos la clave de administrador
    if is_premium:
        register_data["admin_key"] = "astrofuturo_admin_key"

    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=register_data
        )

        if response.status_code == 201:
            user_info = response.json()
            api_key = user_info.get("api_key")
            print(f"Usuario registrado correctamente")
            print(f"API Key: {api_key}")
        else:
            print(f"Error al registrar usuario: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"Error en la solicitud de registro: {str(e)}")
        return

    # Paso 5: Generamos la carta astral
    print("\n=== GENERANDO CARTA ASTRAL ===")

    chart_data = {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_place": birth_location,
        "first_name": first_name,
        "last_name": last_name
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }

    try:
        # Usamos el endpoint adecuado según el tipo de usuario
        endpoint = "/api/astro_chart" if is_premium else "/api/basic_astro_chart"
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            json=chart_data
        )

        if response.status_code == 200:
            chart_info = response.json()
            print("Carta astral generada correctamente:")
            print(f"Tipo de carta: {'Premium' if is_premium else 'Básica'}")
            
            # Mostrar información del zodíaco
            zodiac_info = chart_info.get('zodiac_info', {})
            western_zodiac = zodiac_info.get('western_zodiac', 'No disponible')
            chinese_zodiac = zodiac_info.get('chinese_zodiac', 'No disponible')
            vedic_zodiac = zodiac_info.get('vedic_zodiac', 'No disponible')
            
            print(f"Signo zodiacal occidental: {western_zodiac}")
            
            if is_premium:
                print(f"Signo zodiacal chino: {chinese_zodiac}")
                print(f"Signo zodiacal védico: {vedic_zodiac}")
            
            print("\nExtracto de la carta astral:")
            chart_text = chart_info.get("chart", "")
            print(chart_text[:200] + "..." if len(chart_text) > 200 else chart_text)
            
            # Paso 6: Obtenemos información adicional (zodíaco)
            print("\n=== OBTENIENDO INFORMACIÓN DEL ZODÍACO ===")

            zodiac_data = {
                "date_of_birth": birth_date
            }

            try:
                response = requests.post(
                    f"{BASE_URL}/api/zodiac",
                    headers=headers,
                    json=zodiac_data
                )
                
                if response.status_code == 200:
                    zodiac_info = response.json()
                    print("Información zodiacal completa:")
                    print(f"Signo occidental: {zodiac_info.get('western_zodiac', 'No disponible')}")
                    print(f"Signo chino: {zodiac_info.get('chinese_zodiac', 'No disponible')}")
                    print(f"Signo védico: {zodiac_info.get('vedic_zodiac', 'No disponible')}")
                    print(f"Signo maya: {zodiac_info.get('mayan_zodiac', 'No disponible')}")
                    print(f"Signo egipcio: {zodiac_info.get('egyptian_zodiac', 'No disponible')}")
                    print(f"Signo celta: {zodiac_info.get('celtic_zodiac', 'No disponible')}")
                    print(f"Signo dracónico: {zodiac_info.get('draconic_zodiac', 'No disponible')}")
                    print(f"Signo nativo americano: {zodiac_info.get('native_american_zodiac', 'No disponible')}")
                    
                    # Paso 7: Obtenemos información sobre gemas
                    print("\n=== OBTENIENDO INFORMACIÓN SOBRE GEMAS ===")
                    
                    gemstones_data = {
                        "sign": western_zodiac,
                        "name": full_name,
                        "birth_date": birth_date,
                        "chinese_sign": chinese_zodiac,
                        "vedic_sign": vedic_zodiac
                    }
                    
                    try:
                        response = requests.post(
                            f"{BASE_URL}/api/gemstones",
                            headers=headers,
                            json=gemstones_data
                        )
                        
                        if response.status_code == 200:
                            gemstones_info = response.json()
                            print("Información sobre gemas y cristales:")
                            gemstones_text = gemstones_info.get("gemstones_info", "")
                            print(gemstones_text[:200] + "..." if len(gemstones_text) > 200 else gemstones_text)
                        else:
                            print(f"Error al obtener información sobre gemas: {response.status_code}")
                            print(response.text)
                    except Exception as e:
                        print(f"Error en la solicitud de información sobre gemas: {str(e)}")
                    
                else:
                    print(f"Error al obtener información zodiacal: {response.status_code}")
                    print(response.text)
            except Exception as e:
                print(f"Error en la solicitud de información zodiacal: {str(e)}")
        else:
            print(f"Error al generar carta astral: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"Error en la solicitud de carta astral: {str(e)}")
        return

    print("\n=== PRUEBA COMPLETADA ===\n")

if __name__ == "__main__":
    test_complete_flow()

