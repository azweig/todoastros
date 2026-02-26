from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "up"}), 200

@app.route('/generate', methods=['POST'])
def generate():
    # Obtener datos de la solicitud
    data = request.get_json()
    prompt = data.get('prompt')
    max_tokens = data.get('max_tokens', 1000)
    temperature = data.get('temperature', 0.7)
    
    # Clave API de OpenAI
    api_key = "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"
    
    # URL de la API de OpenAI
    url = "https://api.openai.com/v1/chat/completions"
    
    # Datos para la solicitud
    openai_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Eres un astrólogo experto que escribe cartas astrales detalladas y personalizadas."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    # Cabeceras
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        # Realizar la solicitud
        response = requests.post(url, json=openai_data, headers=headers)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            result = response.json()
            text = result['choices'][0]['message']['content']
            return jsonify({"text": text})
        else:
            return jsonify({"error": f"Error en la API de OpenAI: {response.text}"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/openai/generate', methods=['POST'])
def openai_generate():
    return generate()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
