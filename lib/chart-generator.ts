interface ChartData {
  name: string
  email: string
  birthDate: string
  birthTime?: string
  birthPlace?: string
  plan: "free" | "premium"
}

export async function generateAstralChart(data: ChartData): Promise<string> {
  console.log("Generating chart for:", data)

  try {
    // Simular un retraso para imitar el procesamiento
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // En desarrollo, generamos datos simulados directamente
    const astrologyData = {
      name: data.name,
      date_of_birth: data.birthDate,
      time_of_birth: data.birthTime || "12:00",
      city_of_birth: data.birthPlace || "Unknown",
      responses: {
        zodiac: getSimulatedZodiacData(data.birthDate),
        astronomy: getSimulatedAstronomyData(),
        music: getSimulatedMusicData(data.birthDate),
        weather: getSimulatedWeatherData(),
        news: getSimulatedNewsData(data.birthDate, data.birthPlace || "Unknown"),
        astro_report: getSimulatedAstroReport(data.name, data.birthDate),
      },
    }

    // Codificar los datos para la URL
    const chartDataEncoded = encodeURIComponent(
      JSON.stringify({
        chartData: data,
        astrologyData,
      }),
    )

    // En desarrollo, devolvemos una URL con los datos codificados
    return Promise.resolve(`/view-chart?data=${chartDataEncoded}`)
  } catch (error) {
    console.error("Error generating astral chart:", error)
    throw error
  }
}

// Funciones auxiliares para generar datos simulados
function getSimulatedZodiacData(birthDate: string) {
  const [year, month, day] = birthDate.split("-").map(Number)
  let westernZodiac = "Aries"

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

  return {
    western_zodiac: westernZodiac,
    chinese_zodiac: chineseZodiac,
  }
}

function getSimulatedAstronomyData() {
  return {
    moon_phase: ["Luna Nueva", "Cuarto Creciente", "Luna Llena", "Cuarto Menguante"][Math.floor(Math.random() * 4)],
    planetary_positions: [
      { planet: "Sol", ra: "12h 30m", dec: "23° 26'" },
      { planet: "Luna", ra: "15h 45m", dec: "-18° 15'" },
      { planet: "Mercurio", ra: "10h 20m", dec: "12° 30'" },
      { planet: "Venus", ra: "8h 15m", dec: "-8° 45'" },
      { planet: "Marte", ra: "20h 30m", dec: "15° 20'" },
    ],
  }
}

function getSimulatedMusicData(birthDate: string) {
  const year = Number.parseInt(birthDate.split("-")[0])
  const songs = [
    { rank: 1, song: "Canción Popular #1", artist: "Artista Famoso", date: birthDate },
    { rank: 2, song: "Éxito del Momento", artist: "Grupo Musical", date: birthDate },
    { rank: 3, song: "Balada Romántica", artist: "Cantante Solista", date: birthDate },
    { rank: 4, song: "Tema Bailable", artist: "DJ Internacional", date: birthDate },
    { rank: 5, song: "Canción #5", artist: "Banda de Rock", date: birthDate },
  ]

  return {
    top_songs: songs,
  }
}

function getSimulatedWeatherData() {
  const temperature = Math.floor(Math.random() * 30) + 5
  const descriptions = ["Soleado", "Parcialmente nublado", "Nublado", "Lluvioso"]
  return {
    temperature,
    description: descriptions[Math.floor(Math.random() * descriptions.length)],
  }
}

function getSimulatedNewsData(birthDate: string, birthPlace: string) {
  return {
    city_of_birth: birthPlace,
    date_of_birth: birthDate,
    news_summary: `
En la fecha de tu nacimiento, ${birthDate}, ${birthPlace} vivía momentos interesantes. 
La sociedad experimentaba cambios significativos y el mundo estaba en constante evolución. 
Las estrellas parecían brillar con especial intensidad ese día, como anticipando tu llegada.
    `,
  }
}

function getSimulatedAstroReport(name: string, birthDate: string) {
  return {
    name,
    report: `
Análisis Astrológico para ${name}

Tu carta natal revela una personalidad única y fascinante. La configuración de los astros 
en el momento de tu nacimiento (${birthDate}) ha influido en diferentes aspectos de tu vida, 
creando una combinación especial de energías que te acompañan en tu camino.

Los planetas estaban en una posición particularmente interesante cuando llegaste al mundo, 
sugiriendo una persona con grandes capacidades y un destino especial por delante.

Este análisis es solo una pequeña muestra de la riqueza de información que contiene tu carta astral completa.
    `,
  }
}

