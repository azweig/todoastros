import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave API
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key configurada: {bool(api_key)}")
if api_key:
    print(f"API Key (primeros 5 caracteres): {api_key[:5]}...")
else:
    print("No se encontró la clave API")

# Imprimir todas las variables de entorno
print("\nTodas las variables de entorno:")
for key, value in os.environ.items():
    if "KEY" in key or "SECRET" in key:
        print(f"{key}: {'*' * 10}")
    else:
        print(f"{key}: {value}")
