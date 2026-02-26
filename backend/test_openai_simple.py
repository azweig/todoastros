from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la clave API
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key configurada: {bool(api_key)}")
print(f"API Key (primeros 5 caracteres): {api_key[:5]}...")

try:
    # Crear cliente
    client = OpenAI(api_key=api_key)
    
    # Prueba simple
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello world"}
        ],
        max_tokens=10
    )
    
    print(f"Respuesta: {response.choices[0].message.content}")
    print("¡Prueba exitosa!")
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")
