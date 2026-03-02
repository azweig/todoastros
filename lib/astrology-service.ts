interface AstrologyData {
  name: string
  email: string
  birthDate: string
  birthTime?: string
  birthPlace?: string
  plan: "free" | "premium"
}

interface AstrologyResponse {
  name: string
  date_of_birth: string
  time_of_birth: string
  city_of_birth: string
  responses: {
    zodiac?: {
      western_zodiac: string
      chinese_zodiac: string
    }
    music?: {
      top_songs: Array<{
        rank: number
        song: string
        artist: string
        date: string
      }>
    }
    astronomy?: {
      moon_phase: string
      planetary_positions: Array<{
        planet: string
        ra: string
        dec: string
      }>
    }
    weather?: {
      temperature: number
      description: string
    }
    news?: {
      city_of_birth: string
      date_of_birth: string
      news_summary: string
    }
    astro_report?: {
      name: string
      report: string
    }
  }
  errors?: Record<string, string>
}

export async function generateAstrologyData(data: AstrologyData): Promise<AstrologyResponse | null> {
  try {
    // Llamar a nuestro endpoint seguro en lugar de directamente a los servicios
    const response = await fetch("/api/astrology", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })

    if (response.ok) {
      return await response.json()
    } else {
      console.error("Error from astrology API:", await response.text())
      return generateSimulatedData(data)
    }
  } catch (error) {
    console.error("Error connecting to astrology services:", error)
    return generateSimulatedData(data)
  }
}

// Función para generar datos simulados (se usa tanto en el cliente como en el servidor)
export function generateSimulatedData(data: AstrologyData): AstrologyResponse {
  // Determinar el signo zodiacal basado en la fecha de nacimiento
  const [year, month, day] = data.birthDate.split("-").map(Number)
  let westernZodiac = "Desconocido"

  if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) westernZodiac = "Aries"
  else if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) westernZodiac = "Tauro"
  else if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) westernZodiac = "Géminis"
  else if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) westernZodiac = "Cáncer"
  else if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) westernZodiac = "Leo"
  else if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) westernZodiac = "Virgo"
  else if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) westernZodiac = "Libra"
  else if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) westernZodiac = "Escorpio"
  else if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) westernZodiac = "Sagitario"
  else if ((month === 12 && day >= 22) || (month === 1 && day <= 19)) westernZodiac = "Capricornio"
  else if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) westernZodiac = "Acuario"
  else if ((month === 2 && day >= 19) || (month === 3 && day <= 20)) westernZodiac = "Piscis"

  // Determinar el signo zodiacal chino
  const animals = [
    "Rata",
    "Buey",
    "Tigre",
    "Conejo",
    "Dragón",
    "Serpiente",
    "Caballo",
    "Cabra",
    "Mono",
    "Gallo",
    "Perro",
    "Cerdo",
  ]
  const chineseZodiac = animals[(year - 4) % 12]

  // Generar datos simulados para música
  const topSongs = [
    { rank: 1, song: "Canción Popular #1", artist: "Artista Famoso", date: data.birthDate },
    { rank: 2, song: "Éxito del Momento", artist: "Grupo Musical", date: data.birthDate },
    { rank: 3, song: "Balada Romántica", artist: "Cantante Solista", date: data.birthDate },
    { rank: 4, song: "Tema Bailable", artist: "DJ Internacional", date: data.birthDate },
    { rank: 5, song: "Canción #5", artist: "Banda de Rock", date: data.birthDate },
  ]

  // Generar datos simulados para astronomía
  const moonPhase = ["Luna Nueva", "Cuarto Creciente", "Luna Llena", "Cuarto Menguante"][Math.floor(Math.random() * 4)]
  const planets = ["Sol", "Luna", "Mercurio", "Venus", "Marte", "Júpiter", "Saturno", "Urano", "Neptuno"]
  const planetaryPositions = planets.map((planet) => ({
    planet,
    ra: `${Math.floor(Math.random() * 24)}h ${Math.floor(Math.random() * 60)}m`,
    dec: `${Math.floor(Math.random() * 90)}° ${Math.floor(Math.random() * 60)}'`,
  }))

  // Generar datos simulados para clima
  const temperature = Math.floor(Math.random() * 30) + 5 // Entre 5 y 35 grados
  const weatherDescriptions = ["Soleado", "Parcialmente nublado", "Nublado", "Lluvioso", "Tormentoso"]
  const description = weatherDescriptions[Math.floor(Math.random() * weatherDescriptions.length)]

  // Generar informe astrológico simulado
  const report = `
    Análisis astrológico para ${data.name}:
    
    Tu carta natal revela una personalidad única y fascinante. Nacido bajo el signo de ${westernZodiac}, 
    posees las cualidades características de este signo: ${getZodiacTraits(westernZodiac)}.
    
    La posición de los planetas en el momento de tu nacimiento indica una configuración especial 
    que influye en diferentes aspectos de tu vida. ${getRandomPlanetaryInfluence()}
    
    En la tradición china, perteneces al año del ${chineseZodiac}, lo que añade a tu personalidad 
    rasgos como ${getChineseZodiacTraits(chineseZodiac)}.
    
    El clima en el día de tu nacimiento fue ${description} con una temperatura aproximada de ${temperature}°C, 
    lo que según algunas tradiciones astrológicas, puede influir en ciertos aspectos de tu temperamento.
    
    Este análisis es solo una pequeña muestra de la riqueza de información que contiene tu carta astral completa.
  `

  // Generar resumen de noticias simulado
  const newsSummary = `
    En la fecha de tu nacimiento, ${data.birthDate}, ${data.birthPlace || "tu ciudad natal"} 
    experimentaba un momento especial. ${getRandomHistoricalContext()}
    
    Tu llegada al mundo coincidió con un período de ${getRandomCulturalContext()}, 
    lo que según algunas interpretaciones astrológicas, puede haber influido en tu sensibilidad 
    hacia ciertos temas y tu forma de percibir el mundo.
    
    Las estrellas parecían brillar con especial intensidad ese día, como si celebraran tu nacimiento 
    y anunciaran la llegada de alguien destinado a dejar su huella única en el mundo.
  `

  return {
    name: data.name,
    date_of_birth: data.birthDate,
    time_of_birth: data.birthTime || "12:00",
    city_of_birth: data.birthPlace || "Unknown",
    responses: {
      zodiac: {
        western_zodiac: westernZodiac,
        chinese_zodiac: chineseZodiac,
      },
      music: {
        top_songs: topSongs,
      },
      astronomy: {
        moon_phase: moonPhase,
        planetary_positions: planetaryPositions,
      },
      weather: {
        temperature,
        description,
      },
      news: {
        city_of_birth: data.birthPlace || "Unknown",
        date_of_birth: data.birthDate,
        news_summary: newsSummary,
      },
      astro_report: {
        name: data.name,
        report,
      },
    },
  }
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

function getRandomHistoricalContext(): string {
  const contexts = [
    "la sociedad estaba experimentando importantes cambios culturales que marcarían esa década.",
    "se vivía un momento de optimismo y renovación tras recientes acontecimientos históricos.",
    "el mundo estaba atento a importantes avances científicos y tecnológicos.",
    "se celebraban eventos culturales significativos que dejaron huella en la memoria colectiva.",
    "la ciudad vibraba con una energía especial, como anticipando tu llegada.",
  ]

  return contexts[Math.floor(Math.random() * contexts.length)]
}

function getRandomCulturalContext(): string {
  const contexts = [
    "florecimiento artístico y cultural",
    "innovación y cambio social",
    "reflexión y búsqueda de significado",
    "conexión con las tradiciones y raíces",
    "exploración de nuevas formas de expresión",
  ]

  return contexts[Math.floor(Math.random() * contexts.length)]
}

