// Servicio de noticias integrado en Next.js

interface NewsResponse {
  city_of_birth: string
  date_of_birth: string
  news_summary: string
}

// Función para generar un resumen de noticias basado en la fecha y ciudad
export async function getNewsData(dateOfBirth: string, cityOfBirth: string): Promise<NewsResponse> {
  // En un entorno real, aquí llamaríamos a OpenAI para generar el contenido
  // Para esta implementación, generaremos un texto basado en la fecha y ciudad

  const [year, month, day] = dateOfBirth.split("-").map(Number)

  // Eventos históricos notables por década
  const historicalEvents: Record<string, string[]> = {
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

  // Determinar la década
  let decade = "2020s"
  if (year < 1960) decade = "1950s"
  else if (year < 1970) decade = "1960s"
  else if (year < 1980) decade = "1970s"
  else if (year < 1990) decade = "1980s"
  else if (year < 2000) decade = "1990s"
  else if (year < 2010) decade = "2000s"
  else if (year < 2020) decade = "2010s"

  // Seleccionar un evento histórico basado en el día del mes
  const eventIndex = day % historicalEvents[decade].length
  const historicalEvent = historicalEvents[decade][eventIndex]

  // Generar el resumen de noticias
  const newsSummary = `
En la fecha de tu nacimiento, ${dateOfBirth}, ${cityOfBirth} y el mundo vivían una época fascinante donde ${historicalEvent}.

Tu llegada al mundo coincidió con un momento de transformación y cambio, donde las energías cósmicas parecían alinearse de manera especial. Las estrellas brillaban con particular intensidad ese día, como si celebraran tu nacimiento.

Las personas nacidas en esta época suelen tener una conexión especial con los eventos que definieron ese momento histórico, llevando consigo una sensibilidad única hacia los temas y valores que emergían entonces.

Tu carta astral refleja no solo la posición de los astros en el momento de tu nacimiento, sino también el contexto cultural y social que te recibió, formando una huella única en tu personalidad y destino.
  `

  return {
    city_of_birth: cityOfBirth,
    date_of_birth: dateOfBirth,
    news_summary: newsSummary,
  }
}

