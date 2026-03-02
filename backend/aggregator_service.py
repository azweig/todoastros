from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from base_service import create_service
import requests
import asyncio
import json

app, run = create_service("Aggregator", 5000)

class AggregatorRequest(BaseModel):
    name: str
    birthDate: str
    birthTime: str = None
    birthPlace: str = None
    plan: str = "free"

@app.post("/generate_complete_json")
async def generate_complete_json(request: AggregatorRequest):
    try:
        # Preparar los datos para las solicitudes
        date_of_birth = request.birthDate
        time_of_birth = request.birthTime or "12:00"
        city_of_birth = request.birthPlace or "Unknown"
        
        # Crear diccionario para almacenar respuestas
        responses = {}
        errors = {}
        
        # Función para hacer solicitudes a los servicios
        async def fetch_service(service_name, url, data):
            try:
                response = requests.post(url, json=data, timeout=10)
                if response.status_code == 200:
                    return service_name, response.json()
                else:
                    return service_name, {"error": f"Error {response.status_code}: {response.text}"}
            except Exception as e:
                return service_name, {"error": str(e)}
        
        # Crear tareas para cada servicio
        tasks = []
        
        # Zodiac service
        tasks.append(fetch_service(
            "zodiac", 
            "http://localhost:5001/zodiac", 
            {"date_of_birth": date_of_birth}
        ))
        
        # Astronomy service
        tasks.append(fetch_service(
            "astronomy", 
            "http://localhost:5003/astronomy", 
            {
                "date_of_birth": date_of_birth,
                "time_of_birth": time_of_birth,
                "city_of_birth": city_of_birth
            }
        ))
        
        # Astro report service
        tasks.append(fetch_service(
            "astro_report", 
            "http://localhost:5006/astro_report", 
            {
                "name": request.name,
                "date_of_birth": date_of_birth,
                "time_of_birth": time_of_birth,
                "city_of_birth": city_of_birth
            }
        ))
        
        # Si es plan premium, agregar servicios adicionales
        if request.plan == "premium":
            # Music service
            tasks.append(fetch_service(
                "music", 
                "http://localhost:5002/music", 
                {"date_of_birth": date_of_birth}
            ))
            
            # Weather service
            tasks.append(fetch_service(
                "weather", 
                "http://localhost:5004/weather", 
                {
                    "date_of_birth": date_of_birth,
                    "city_of_birth": city_of_birth
                }
            ))
            
            # News service
            tasks.append(fetch_service(
                "news", 
                "http://localhost:5007/news", 
                {
                    "date_of_birth": date_of_birth,
                    "city_of_birth": city_of_birth
                }
            ))
        
        # Ejecutar todas las tareas concurrentemente
        results = await asyncio.gather(*tasks)
        
        # Procesar resultados
        for service_name, result in results:
            if "error" in result:
                errors[service_name] = result["error"]
            else:
                responses[service_name] = result
        
        # Construir respuesta final
        response_data = {
            "name": request.name,
            "date_of_birth": date_of_birth,
            "time_of_birth": time_of_birth,
            "city_of_birth": city_of_birth,
            "responses": responses
        }
        
        if errors:
            response_data["errors"] = errors
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    run()

