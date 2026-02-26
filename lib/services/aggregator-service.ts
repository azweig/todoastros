// Servicio agregador que combina todos los servicios astrológicos

import { getZodiacSign } from "./zodiac-service"
import { getAstronomicalData } from "./astronomy-service"
import { getPopularMusic } from "./music-service"
import { getWeatherData } from "./weather-service"
import { getNewsData } from "./news-service"
import { getAstroReport } from "./astro-report-service"

interface AggregatorRequest {
  name: string
  birthDate: string
  birthTime?: string
  birthPlace?: string
  plan: "free" | "premium"
}

interface AggregatorResponse {
  name: string
  date_of_birth: string
  time_of_birth: string
  city_of_birth: string
  responses: {
    zodiac: ReturnType<typeof getZodiacSign>
    astronomy: ReturnType<typeof getAstronomicalData>
    music: {
      top_songs: Array<{
        rank: number
        song: string
        artist: string
        date: string
      }>
    }
    weather: ReturnType<typeof getWeatherData>
    news: Awaited<ReturnType<typeof getNewsData>>
    astro_report: Awaited<ReturnType<typeof getAstroReport>>
  }
}

export async function generateCompleteAstrology(data: AggregatorRequest): Promise<AggregatorResponse> {
  // Obtener datos de todos los servicios
  const zodiacData = getZodiacSign(data.birthDate)
  const astronomyData = getAstronomicalData(data.birthDate)
  const musicData = getPopularMusic(data.birthDate)
  const weatherData = getWeatherData(data.birthDate, data.birthPlace || "Unknown")
  const newsData = await getNewsData(data.birthDate, data.birthPlace || "Unknown")
  const reportData = await getAstroReport(
    data.name,
    data.birthDate,
    data.birthTime || "12:00",
    data.birthPlace || "Unknown",
  )

  // Combinar todos los datos en una respuesta
  return {
    name: data.name,
    date_of_birth: data.birthDate,
    time_of_birth: data.birthTime || "12:00",
    city_of_birth: data.birthPlace || "Unknown",
    responses: {
      zodiac: zodiacData,
      astronomy: astronomyData,
      music: musicData,
      weather: weatherData,
      news: newsData,
      astro_report: reportData,
    },
  }
}

