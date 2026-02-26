import os
import sys
import requests

# Clave API de OpenAI
api_key = "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"

# URL de la API de OpenAI
url = "https://api.openai.com/v1/chat/completions"

# Datos para la solicitud
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello world"}
    ],
    "max_tokens": 10
}

# Cabeceras
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

try:
    # Realizar la solicitud
    response = requests.post(url, json=data, headers=headers)
    
    # Imprimir la respuesta
    print(f"Código de estado: {response.status_code}")
    print(f"Respuesta: {response.json()}")
except Exception as e:
    print(f"Error: {str(e)}")
