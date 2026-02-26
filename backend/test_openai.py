import os
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key configurada: {bool(openai.api_key)}")
print(f"API Key: {openai.api_key[:5]}...{openai.api_key[-5:]}")

try:
    # Generar texto con OpenAI - versión simple
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Usamos un modelo más simple para pruebas
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Dime hola mundo"}
        ],
        max_tokens=20
    )
    
    # Extraer el texto generado
    generated_text = response.choices[0].message.content
    print(f"Texto generado: {generated_text}")
    print("¡Prueba exitosa!")
    
except Exception as e:
    print(f"Error al generar texto: {str(e)}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")
