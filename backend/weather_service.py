from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from base_service import create_service
from datetime import datetime

app, run = create_service("Weather", 5004)

class WeatherRequest(BaseModel):
    date_of_birth: str
    city_of_birth: str = None

@app.post("/weather")
async def get_weather(request: WeatherRequest):
    try:
        # Convertir la fecha de nacimiento a objeto datetime
        birth_date = datetime.strptime(request.date_of_birth, "%Y-%m-%d")
        city = request.city_of_birth or "Unknown"
        
        # Usar la fecha y ciudad como semilla para generar datos "deterministas"
        date_seed = birth_date.toordinal()
        city_seed = sum(ord(c) for c in city)
        combined_seed = (date_seed + city_seed) % 100000
        
        # Generar temperatura basada en la semilla (entre 5°C y 35°C)
        temperature = 5 + (combined_seed % 30)
        
        # Determinar descripción del clima basada en la temperatura
        if temperature < 10:
            description = "Frío"
        elif temperature < 15:
            description = "Fresco"
        elif temperature < 20:
            description = "Templado"
        elif temperature < 25:
            description = "Cálido"
        elif temperature < 30:
            description = "Caluroso"
        else:
            description = "Muy caluroso"
        
        # Añadir condiciones climáticas basadas en el resto de la semilla
        conditions = combined_seed % 5
        if conditions == 0:
            description += " y soleado"
        elif conditions == 1:
            description += " y parcialmente nublado"
        elif conditions == 2:
            description += " y nublado"
        elif conditions == 3:
            description += " con lluvia ligera"
        else:
            description += " con tormentas"
        
        return {
            "temperature": temperature,
            "description": description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    run()

