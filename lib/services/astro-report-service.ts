// Servicio de informes astrológicos integrado en Next.js
import { getZodiacSign } from "./zodiac-service"
import { getAstronomicalData } from "./astronomy-service"
import { getWeatherData } from "./weather-service"

interface AstroReportResponse {
  name: string
  report: string
}

// Función para generar un informe astrológico
export async function getAstroReport(
  name: string,
  dateOfBirth: string,
  timeOfBirth = "12:00",
  cityOfBirth = "Unknown",
): Promise<AstroReportResponse> {
  try {
    // Obtener datos básicos para enriquecer el informe
    const zodiacData = getZodiacSign(dateOfBirth)
    const astronomyData = getAstronomicalData(dateOfBirth)
    const weatherData = getWeatherData(dateOfBirth, cityOfBirth)

    // Generar informe local
    return {
      name,
      report: generateLocalReport(name, dateOfBirth, timeOfBirth, cityOfBirth, zodiacData, astronomyData, weatherData),
    }
  } catch (error) {
    console.error("Error in astro report service:", error)
    // En caso de error, devolver un informe básico
    return {
      name,
      report: `
Análisis astrológico para ${name}:

Tu carta natal revela una personalidad única y fascinante. Nacido bajo el signo de ${getZodiacSign(dateOfBirth).western_zodiac}, 
posees cualidades especiales que te distinguen y te guían en tu camino de vida.

La posición de los astros en el momento de tu nacimiento ha influido en diferentes aspectos de tu personalidad,
creando una configuración única que te acompaña a lo largo de tu existencia.

Este análisis es solo una pequeña muestra de la riqueza de información que contiene tu carta astral completa.
      `,
    }
  }
}

// Función para generar un informe localmente
function generateLocalReport(
  name: string,
  dateOfBirth: string,
  timeOfBirth: string,
  cityOfBirth: string,
  zodiacData: ReturnType<typeof getZodiacSign>,
  astronomyData: ReturnType<typeof getAstronomicalData>,
  weatherData: ReturnType<typeof getWeatherData>,
): string {
  // Obtener rasgos del signo zodiacal
  const zodiacTraits = getZodiacTraits(zodiacData.western_zodiac)
  const chineseTraits = getChineseZodiacTraits(zodiacData.chinese_zodiac)

  // Generar influencias planetarias
  const planetaryInfluence = getRandomPlanetaryInfluence()

  // Generar el informe
  return `
Análisis Astrológico para ${name}

Querido/a ${name},

Tu carta astral es un mapa celestial único que captura el momento exacto en que llegaste a este mundo. Nacido/a el ${dateOfBirth} a las ${timeOfBirth} en ${cityOfBirth}, los astros te recibieron con una configuración especial que ha influido en tu esencia y en tu camino de vida.

PERFIL ZODIACAL:
Como ${zodiacData.western_zodiac}, tu naturaleza se caracteriza por ${zodiacTraits}. Esta energía fundamental forma la base de tu personalidad y se manifiesta en la forma en que te relacionas con el mundo y con los demás.

En la tradición china, perteneces al año del ${zodiacData.chinese_zodiac}, lo que añade a tu personalidad rasgos como ${chineseTraits}. Esta influencia complementa tu signo occidental, creando una combinación única de energías.

INFLUENCIAS PLANETARIAS:
En el momento de tu nacimiento, la Luna se encontraba en fase de ${astronomyData.moon_phase}, lo que influye en tu mundo emocional y en tu conexión con tu intuición. ${planetaryInfluence}

ELEMENTOS CONTEXTUALES:
El clima en el día de tu nacimiento fue ${weatherData.description} con una temperatura aproximada de ${weatherData.temperature}°C. Según algunas tradiciones astrológicas, las condiciones climáticas en el momento del nacimiento pueden influir sutilmente en el temperamento y en ciertas predisposiciones energéticas.

CONSEJOS PARA TU CAMINO:
1. Aprovecha tus fortalezas naturales como ${zodiacData.western_zodiac}, especialmente tu ${getZodiacStrength(zodiacData.western_zodiac)}.
2. Trabaja conscientemente en equilibrar tu tendencia hacia ${getZodiacChallenge(zodiacData.western_zodiac)}.
3. Los momentos de ${astronomyData.moon_phase} lunar pueden ser especialmente propicios para la introspección y la renovación personal.

CONCLUSIÓN:
Tu carta astral revela un potencial único y un camino lleno de posibilidades. Recuerda que las estrellas inclinan pero no obligan; tu libre albedrío y tus decisiones conscientes son siempre la fuerza más poderosa en la creación de tu destino.

Este análisis es solo una pequeña muestra de la riqueza de información que contiene tu carta astral completa. Te invitamos a profundizar en este conocimiento ancestral que puede ofrecerte valiosas perspectivas sobre tu viaje personal.

Con luz estelar,
AstroFuturo
  `
}

// Funciones auxiliares para generar texto descriptivo
function getZodiacTraits(zodiac: string): string {
  const traits: Record<string, string> = {
    Aries: "energía, iniciativa y valentía",
    Tauro: "determinación, sensualidad y practicidad",
    Géminis: "curiosidad, adaptabilidad y comunicación",
    Cáncer: "intuición, sensibilidad y protección",
    Leo: "creatividad, generosidad y liderazgo",
    Virgo: "análisis, perfeccionismo y servicio",
    Libra: "equilibrio, diplomacia y apreciación por la belleza",
    Escorpio: "intensidad, pasión y transformación",
    Sagitario: "optimismo, libertad y búsqueda de la verdad",
    Capricornio: "ambición, disciplina y responsabilidad",
    Acuario: "originalidad, independencia y visión de futuro",
    Piscis: "compasión, intuición y conexión espiritual",
  }

  return traits[zodiac] || "cualidades únicas y especiales"
}

function getZodiacStrength(zodiac: string): string {
  const strengths: Record<string, string> = {
    Aries: "valentía y capacidad de iniciativa",
    Tauro: "determinación y sentido práctico",
    Géminis: "versatilidad y habilidades comunicativas",
    Cáncer: "intuición y capacidad de cuidar a otros",
    Leo: "confianza y generosidad",
    Virgo: "atención al detalle y capacidad analítica",
    Libra: "diplomacia y sentido de la justicia",
    Escorpio: "intensidad emocional y capacidad de transformación",
    Sagitario: "optimismo y visión expansiva",
    Capricornio: "disciplina y sentido de la responsabilidad",
    Acuario: "originalidad y pensamiento innovador",
    Piscis: "compasión y conexión espiritual",
  }

  return strengths[zodiac] || "capacidad de adaptación"
}

function getZodiacChallenge(zodiac: string): string {
  const challenges: Record<string, string> = {
    Aries: "la impulsividad y la impaciencia",
    Tauro: "la terquedad y la resistencia al cambio",
    Géminis: "la dispersión y la inconsistencia",
    Cáncer: "la hipersensibilidad y el apego excesivo",
    Leo: "el orgullo y la necesidad de reconocimiento",
    Virgo: "el perfeccionismo y la autocrítica",
    Libra: "la indecisión y la evitación del conflicto",
    Escorpio: "los celos y el control",
    Sagitario: "la imprudencia y la falta de tacto",
    Capricornio: "el pesimismo y la rigidez",
    Acuario: "el distanciamiento emocional y la rebeldía",
    Piscis: "la evasión y la confusión de límites",
  }

  return challenges[zodiac] || "los desafíos que se presentan en tu camino"
}

function getChineseZodiacTraits(animal: string): string {
  const traits: Record<string, string> = {
    Rata: "ingenio, adaptabilidad y vitalidad",
    Buey: "diligencia, confiabilidad y determinación",
    Tigre: "valentía, competitividad y carisma",
    Conejo: "compasión, elegancia y prudencia",
    Dragón: "entusiasmo, confianza y ambición",
    Serpiente: "intuición, sabiduría y elegancia",
    Caballo: "energía, independencia y sociabilidad",
    Cabra: "creatividad, empatía y sensibilidad",
    Mono: "inteligencia, curiosidad y versatilidad",
    Gallo: "observación, honestidad y meticulosidad",
    Perro: "lealtad, justicia y altruismo",
    Cerdo: "generosidad, sinceridad y disfrute de la vida",
  }

  return traits[animal] || "cualidades únicas y especiales"
}

function getRandomPlanetaryInfluence(): string {
  const influences = [
    "Mercurio en tu carta sugiere una mente analítica y una gran capacidad de comunicación.",
    "Venus en una posición favorable indica una naturaleza artística y una gran capacidad para las relaciones personales.",
    "La influencia de Marte te otorga determinación y energía para perseguir tus objetivos.",
    "Júpiter bien aspectado sugiere oportunidades de crecimiento y expansión en tu vida.",
    "La presencia de Saturno te brinda disciplina y capacidad para construir estructuras sólidas.",
    "Urano en tu carta indica originalidad y capacidad para romper con lo establecido.",
    "Neptuno influye en tu sensibilidad espiritual y capacidad imaginativa.",
    "Plutón te conecta con procesos de transformación profunda y regeneración.",
  ]

  return influences[Math.floor(Math.random() * influences.length)]
}

