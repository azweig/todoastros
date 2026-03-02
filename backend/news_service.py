from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from base_service import create_service
from datetime import datetime
import uvicorn

app, run = create_service("News", 5007)

class NewsRequest(BaseModel):
    date_of_birth: str
    city_of_birth: str = None

# Eventos históricos notables por década
historical_events = {
    "1950s": [
        "la televisión comenzaba a transformar la sociedad",
        "el mundo se recuperaba de la Segunda Guerra Mundial",
        "comenzaba la era espacial con el lanzamiento del Sputnik",
        "el rock and roll revolucionaba la música popular",
    ],
    "1960s": [
        "el movimiento por los derechos civiles ganaba fuerza",
        "la humanidad daba sus primeros pasos en la Luna",
        "la cultura hippie florecía con mensajes de paz y amor",
        "la música de The Beatles transformaba la cultura juvenil",
    ],
    "1970s": [
        "la crisis del petróleo afectaba la economía mundial",
        "la música disco dominaba las pistas de baile",
        "las computadoras personales comenzaban a desarrollarse",
        "el movimiento ecologista ganaba impulso",
    ],
    "1980s": [
        "la revolución tecnológica comenzaba a transformar la sociedad",
        "la música pop alcanzaba nuevas alturas de popularidad",
        "el mundo vivía los últimos años de la Guerra Fría",
        "la moda y la cultura experimentaban un período de exuberancia",
    ],
    "1990s": [
        "Internet comenzaba a cambiar la forma en que nos comunicamos",
        "la música grunge y el hip-hop definían nuevas identidades culturales",
        "el mundo celebraba el fin del milenio con grandes expectativas",
        "la globalización aceleraba el intercambio cultural entre naciones",
    ],
    "2000s": [
        "la revolución digital transformaba todos los aspectos de la vida cotidiana",
        "las redes sociales comenzaban a conectar personas de todo el mundo",
        "los smartphones iniciaban una nueva era de comunicación móvil",
        "la música y el arte exploraban nuevas formas de expresión digital",
    ],
    "2010s": [
        "las redes sociales se convertían en el centro de la vida social",
        "el streaming transformaba el consumo de música y entretenimiento",
        "los movimientos sociales utilizaban internet para organizarse globalmente",
        "la inteligencia artificial comenzaba a integrarse en la vida cotidiana",
    ],
    "2020s": [
        "el mundo enfrentaba desafíos globales sin precedentes",
        "la tecnología permitía nuevas formas de trabajo y conexión a distancia",
        "la conciencia sobre el cambio climático alcanzaba niveles históricos",
        "la inteligencia artificial transformaba industrias enteras",
    ],
}

@app.post("/news")
async def get_news(request: NewsRequest):
    try:
        # Convertir la fecha de nacimiento a objeto datetime
        birth_date = datetime.strptime(request.date_of_birth, "%Y-%m-%d")
        city = request.city_of_birth or "tu lugar de nacimiento"
        year = birth_date.year
        
        # Determinar la década
        decade = None
        if year < 1960:
            decade = "1950s"
        elif year < 1970:
            decade = "1960s"
        elif year < 1980:
            decade = "1970s"
        elif year < 1990:
            decade = "1980s"
        elif year < 2000:
            decade = "1990s"
        elif year < 2010:
            decade = "2010s"
        else:
            decade = "2020s"
        
        # Seleccionar un evento histórico basado en el día del mes
        day = birth_date.day
        event_index = day % len(historical_events[decade])
        historical_event = historical_events[decade][event_index]
        
        # Generar el resumen de noticias
        news_summary = f"""
En la fecha de tu nacimiento, {request.date_of_birth}, {city} y el mundo vivían una época fascinante donde {historical_event}.

Tu llegada al mundo coincidió con un momento de transformación y cambio, donde las energías cósmicas parecían alinearse de manera especial. Las estrellas brillaban con particular intensidad ese día, como si celebraran tu nacimiento.

Las personas nacidas en esta época suelen tener una conexión especial con los eventos que definieron ese momento histórico, llevando consigo una sensibilidad única hacia los temas y valores que emergían entonces.

Tu carta astral refleja no solo la posición de los astros en el momento de tu nacimiento, sino también el contexto cultural y social que te recibió, formando una huella única en tu personalidad y destino.
        """
        
        return {
            "city_of_birth": city,
            "date_of_birth": request.date_of_birth,
            "news_summary": news_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Modificar la línea en la función run() para escuchar en todas las interfaces
def run():
    """Ejecuta el servicio en el puerto especificado"""
    uvicorn.run(app, host="0.0.0.0", port=5007)

if __name__ == "__main__":
    run()

