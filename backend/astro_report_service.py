from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from base_service import create_service
import requests
from datetime import datetime
import uvicorn

app, run = create_service("Astro Report", 5006)

class ReportRequest(BaseModel):
    name: str
    date_of_birth: str
    time_of_birth: str = None
    city_of_birth: str = None

# Funciones auxiliares para generar texto descriptivo
def get_zodiac_traits(zodiac):
    traits = {
        "Aries": "energía, iniciativa y valentía",
        "Tauro": "determinación, sensualidad y practicidad",
        "Géminis": "curiosidad, adaptabilidad y comunicación",
        "Cáncer": "intuición, sensibilidad y protección",
        "Leo": "creatividad, generosidad y liderazgo",
        "Virgo": "análisis, perfeccionismo y servicio",
        "Libra": "equilibrio, diplomacia y apreciación por la belleza",
        "Escorpio": "intensidad, pasión y transformación",
        "Sagitario": "optimismo, libertad y búsqueda de la verdad",
        "Capricornio": "ambición, disciplina y responsabilidad",
        "Acuario": "originalidad, independencia y visión de futuro",
        "Piscis": "compasión, intuición y conexión espiritual",
    }
    return traits.get(zodiac, "cualidades únicas y especiales")

def get_zodiac_strength(zodiac):
    strengths = {
        "Aries": "valentía y capacidad de iniciativa",
        "Tauro": "determinación y sentido práctico",
        "Géminis": "versatilidad y habilidades comunicativas",
        "Cáncer": "intuición y capacidad de cuidar a otros",
        "Leo": "confianza y generosidad",
        "Virgo": "atención al detalle y capacidad analítica",
        "Libra": "diplomacia y sentido de la justicia",
        "Escorpio": "intensidad emocional y capacidad de transformación",
        "Sagitario": "optimismo y visión expansiva",
        "Capricornio": "disciplina y sentido de la responsabilidad",
        "Acuario": "originalidad y pensamiento innovador",
        "Piscis": "compasión y conexión espiritual",
    }
    return strengths.get(zodiac, "capacidad de adaptación")

def get_zodiac_challenge(zodiac):
    challenges = {
        "Aries": "la impulsividad y la impaciencia",
        "Tauro": "la terquedad y la resistencia al cambio",
        "Géminis": "la dispersión y la inconsistencia",
        "Cáncer": "la hipersensibilidad y el apego excesivo",
        "Leo": "el orgullo y la necesidad de reconocimiento",
        "Virgo": "el perfeccionismo y la autocrítica",
        "Libra": "la indecisión y la evitación del conflicto",
        "Escorpio": "los celos y el control",
        "Sagitario": "la imprudencia y la falta de tacto",
        "Capricornio": "el pesimismo y la rigidez",
        "Acuario": "el distanciamiento emocional y la rebeldía",
        "Piscis": "la evasión y la confusión de límites",
    }
    return challenges.get(zodiac, "los desafíos que se presentan en tu camino")

def get_chinese_zodiac_traits(animal):
    traits = {
        "Rata": "ingenio, adaptabilidad y vitalidad",
        "Buey": "diligencia, confiabilidad y determinación",
        "Tigre": "valentía, competitividad y carisma",
        "Conejo": "compasión, elegancia y prudencia",
        "Dragón": "entusiasmo, confianza y ambición",
        "Serpiente": "intuición, sabiduría y elegancia",
        "Caballo": "energía, independencia y sociabilidad",
        "Cabra": "creatividad, empatía y sensibilidad",
        "Mono": "inteligencia, curiosidad y versatilidad",
        "Gallo": "observación, honestidad y meticulosidad",
        "Perro": "lealtad, justicia y altruismo",
        "Cerdo": "generosidad, sinceridad y disfrute de la vida",
    }
    return traits.get(animal, "cualidades únicas y especiales")

def get_random_planetary_influence():
    influences = [
        "Mercurio en tu carta sugiere una mente analítica y una gran capacidad de comunicación.",
        "Venus en una posición favorable indica una naturaleza artística y una gran capacidad para las relaciones personales.",
        "La influencia de Marte te otorga determinación y energía para perseguir tus objetivos.",
        "Júpiter bien aspectado sugiere oportunidades de crecimiento y expansión en tu vida.",
        "La presencia de Saturno te brinda disciplina y capacidad para construir estructuras sólidas.",
        "Urano en tu carta indica originalidad y capacidad para romper con lo establecido.",
        "Neptuno influye en tu sensibilidad espiritual y capacidad imaginativa.",
        "Plutón te conecta con procesos de transformación profunda y regeneración.",
    ]
    import random
    return influences[random.randint(0, len(influences) - 1)]

@app.post("/astro_report")
async def get_astro_report(request: ReportRequest):
    try:
        # Obtener el signo zodiacal
        try:
            zodiac_response = requests.post(
                "http://localhost:5001/zodiac",
                json={"date_of_birth": request.date_of_birth},
                timeout=5
            )
            zodiac_data = zodiac_response.json()
            western_zodiac = zodiac_data["western_zodiac"]
            chinese_zodiac = zodiac_data["chinese_zodiac"]
        except:
            # Si no se puede conectar al servicio de zodíaco, calcular manualmente
            birth_date = datetime.strptime(request.date_of_birth, "%Y-%m-%d")
            month, day, year = birth_date.month, birth_date.day, birth_date.year
            
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
                
            animals = ["Rata", "Buey", "Tigre", "Conejo", "Dragón", "Serpiente", 
                      "Caballo", "Cabra", "Mono", "Gallo", "Perro", "Cerdo"]
            chinese_zodiac = animals[(year - 4) % 12]
        
        # Obtener datos de astronomía
        try:
            astronomy_response = requests.post(
                "http://localhost:5003/astronomy",
                json={
                    "date_of_birth": request.date_of_birth,
                    "time_of_birth": request.time_of_birth,
                    "city_of_birth": request.city_of_birth
                },
                timeout=5
            )
            astronomy_data = astronomy_response.json()
            moon_phase = astronomy_data["moon_phase"]
        except:
            # Si no se puede conectar al servicio de astronomía, usar valor predeterminado
            moon_phase = "Luna Llena"
        
        # Generar informe astrológico
        zodiac_traits = get_zodiac_traits(western_zodiac)
        zodiac_strength = get_zodiac_strength(western_zodiac)
        zodiac_challenge = get_zodiac_challenge(western_zodiac)
        chinese_traits = get_chinese_zodiac_traits(chinese_zodiac)
        planetary_influence = get_random_planetary_influence()
        
        report = f"""
Análisis Astrológico para {request.name}

Querido/a {request.name},

Tu carta astral es un mapa celestial único que captura el momento exacto en que llegaste a este mundo. Nacido/a el {request.date_of_birth} a las {request.time_of_birth or "12:00"} en {request.city_of_birth or "tu ciudad natal"}, los astros te recibieron con una configuración especial que ha influido en tu esencia y en tu camino de vida.

PERFIL ZODIACAL:
Como {western_zodiac}, tu naturaleza se caracteriza por {zodiac_traits}. Esta energía fundamental forma la base de tu personalidad y se manifiesta en la forma en que te relacionas con el mundo y con los demás.

En la tradición china, perteneces al año del {chinese_zodiac}, lo que añade a tu personalidad rasgos como {chinese_traits}. Esta influencia complementa tu signo occidental, creando una combinación única de energías.

INFLUENCIAS PLANETARIAS:
En el momento de tu nacimiento, la Luna se encontraba en fase de {moon_phase}, lo que influye en tu mundo emocional y en tu conexión con tu intuición. {planetary_influence}

CONSEJOS PARA TU CAMINO:
1. Aprovecha tus fortalezas naturales como {western_zodiac}, especialmente tu {zodiac_strength}.
2. Trabaja conscientemente en equilibrar tu tendencia hacia {zodiac_challenge}.
3. Los momentos de {moon_phase} lunar pueden ser especialmente propicios para la introspección y la renovación personal.

CONCLUSIÓN:
Tu carta astral revela un potencial único y un camino lleno de posibilidades. Recuerda que las estrellas inclinan pero no obligan; tu libre albedrío y tus decisiones conscientes son siempre la fuerza más poderosa en la creación de tu destino.

Este análisis es solo una pequeña muestra de la riqueza de información que contiene tu carta astral completa. Te invitamos a profundizar en este conocimiento ancestral que puede ofrecerte valiosas perspectivas sobre tu viaje personal.

Con luz estelar,
AstroFuturo
"""
        
        return {
            "name": request.name,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run():
    """Ejecuta el servicio en el puerto especificado"""
    uvicorn.run(app, host="0.0.0.0", port=5006)

if __name__ == "__main__":
    run()

