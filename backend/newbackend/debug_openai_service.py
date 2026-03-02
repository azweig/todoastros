import requests
import json
import sys

def test_openai_service():
    """
    Script para probar el servicio de OpenAI y diagnosticar problemas
    """
    print("\n=== DIAGNÓSTICO DEL SERVICIO OPENAI ===\n")
    
    # 1. Verificar si el servicio está en ejecución
    try:
        response = requests.get("http://openai_service:5010/health", timeout=5)
        print(f"Estado del servicio: {response.status_code}")
        print(f"Respuesta: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servicio: {str(e)}")
        print("\nPosibles problemas:")
        print("1. El servicio openai_service no está en ejecución")
        print("2. El puerto 5010 no está expuesto correctamente")
        print("3. Hay un problema de red en Docker")
        
        # Sugerir comandos para verificar
        print("\nEjecuta estos comandos para verificar:")
        print("docker-compose ps")
        print("docker-compose logs openai_service")
        print("docker network inspect newbackend_default")
        
        # Intentar resolver el nombre de host
        print("\nVerificando resolución de nombres:")
        import socket
        try:
            print(f"Resolución de 'openai_service': {socket.gethostbyname('openai_service')}")
        except socket.gaierror:
            print("No se puede resolver el nombre 'openai_service'")
        
        return
    
    # 2. Probar una solicitud simple
    print("\nProbando solicitud simple al servicio OpenAI:")
    
    test_data = {
        "prompt": "Hola, ¿cómo estás?",
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "http://openai_service:5010/generate",
            json=test_data,
            timeout=10
        )
        
        print(f"Código de respuesta: {response.status_code}")
        if response.status_code == 200:
            print("Respuesta exitosa:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {str(e)}")
    
    # 3. Verificar configuración
    print("\nVerificando configuración del servicio:")
    print("Este script debe ejecutarse dentro del contenedor del API Gateway o en un contenedor")
    print("que esté en la misma red Docker que el servicio OpenAI.")
    
    print("\nPara ejecutar este script dentro del contenedor del API Gateway:")
    print("docker-compose exec api_gateway python /ruta/a/este/script.py")
    
    # 4. Verificar variables de entorno
    print("\nVerificando variables de entorno en el servicio de gemas:")
    print("Ejecuta este comando para ver las variables de entorno:")
    print("docker-compose exec gemstones_service env | grep OPENAI")

if __name__ == "__main__":
    test_openai_service()

