from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from base_service import create_service
from datetime import datetime

app, run = create_service("Zodiac", 5001)

class ZodiacRequest(BaseModel):
    date_of_birth: str

@app.post("/zodiac")
async def get_zodiac(request: ZodiacRequest):
    try:
        # Convertir la fecha de nacimiento a objeto datetime
        birth_date = datetime.strptime(request.date_of_birth, "%Y-%m-%d")
        
        # Determinar el signo zodiacal occidental
        month = birth_date.month
        day = birth_date.day
        
        western_zodiac = ""
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            western_zodiac = "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            western_zodiac = "Tauro"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            western_zodiac = "Géminis"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            western_zodiac = "Cáncer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            western_zodiac = "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            western_zodiac = "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            western_zodiac = "Libra"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            western_zodiac = "Escorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            western_zodiac = "Sagitario"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            western_zodiac = "Capricornio"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            western_zodiac = "Acuario"
        else:
            western_zodiac = "Piscis"
        
        # Determinar el signo zodiacal chino
        year = birth_date.year
        animals = ["Rata", "Buey", "Tigre", "Conejo", "Dragón", "Serpiente", 
                  "Caballo", "Cabra", "Mono", "Gallo", "Perro", "Cerdo"]
        chinese_zodiac = animals[(year - 4) % 12]
        
        return {
            "western_zodiac": western_zodiac,
            "chinese_zodiac": chinese_zodiac
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    run()

