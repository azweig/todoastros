from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from base_service import create_service
from datetime import datetime
import random

app, run = create_service("Astronomy", 5003)

class AstronomyRequest(BaseModel):
    date_of_birth: str
    time_of_birth: str = None
    city_of_birth: str = None

@app.post("/astronomy")
async def get_astronomy(request: AstronomyRequest):
    try:
        # Convertir la fecha de nacimiento a objeto datetime
        birth_date = datetime.strptime(request.date_of_birth, "%Y-%m-%d")
        
        # Determinar la fase lunar basada en el día del mes
        day = birth_date.day
        if day < 8:
            moon_phase = "Luna Nueva"
        elif day < 15:
            moon_phase = "Cuarto Creciente"
        elif day < 22:
            moon_phase = "Luna Llena"
        else:
            moon_phase = "Cuarto Menguante"
        
        # Generar posiciones planetarias simuladas
        planets = ["Sol", "Luna", "Mercurio", "Venus", "Marte", "Júpiter", "Saturno", "Urano", "Neptuno"]
        planetary_positions = []
        
        for planet in planets:
            # Usar el nombre del planeta y la fecha como semilla para generar posiciones "deterministas"
            seed = sum(ord(c) for c in planet)
            date_seed = birth_date.toordinal()
            combined_seed = (seed + date_seed) % 1000
            
            # Generar valores basados en la semilla
            ra = f"{combined_seed % 24}h {combined_seed % 60}m"
            dec = f"{combined_seed % 90}° {combined_seed % 60}'"
            
            planetary_positions.append({
                "planet": planet,
                "ra": ra,
                "dec": dec
            })
        
        return {
            "moon_phase": moon_phase,
            "planetary_positions": planetary_positions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    run()

