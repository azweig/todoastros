import { type NextRequest, NextResponse } from "next/server"
import { generateCompleteAstrology } from "@/lib/services/aggregator-service"

export async function POST(request: NextRequest) {
  try {
    const data = await request.json()

    // Validar datos de entrada
    if (!data.name || !data.birthDate) {
      return NextResponse.json({ error: "Faltan datos obligatorios: name, birthDate" }, { status: 400 })
    }

    // Generar datos astrológicos completos
    const result = await generateCompleteAstrology({
      name: data.name,
      birthDate: data.birthDate,
      birthTime: data.birthTime,
      birthPlace: data.birthPlace,
      plan: data.plan || "free",
    })

    return NextResponse.json(result)
  } catch (error) {
    console.error("Error processing astrology data:", error)

    // En caso de error, devolver datos simulados
    const requestBody = await request.json()
    const simulatedData = {
      name: requestBody.name,
      date_of_birth: requestBody.birthDate,
      time_of_birth: requestBody.birthTime || "12:00",
      city_of_birth: requestBody.birthPlace || "Unknown",
      responses: {
        zodiac: getSimulatedZodiacData(requestBody.birthDate),
        astronomy: getSimulatedAstronomyData(),
        music: getSimulatedMusicData(requestBody.birthDate),
        weather: getSimulatedWeatherData(),
        news: getSimulatedNewsData(requestBody.birthDate, requestBody.birthPlace || "Unknown"),
        astro_report: getSimulatedAstroReport(requestBody.name, requestBody.birthDate),
      },
    }

    return NextResponse.json(simulatedData)
  }
}

// Reutilizar las mismas funciones de simulación que definimos en chart-generator.ts
function getSimulatedZodiacData(birthDate: string) {
  const zodiacSigns = [
    { name: "Aries", start: "03-21", end: "04-19" },
    { name: "Taurus", start: "04-20", end: "05-20" },
    { name: "Gemini", start: "05-21", end: "06-20" },
    { name: "Cancer", start: "06-21", end: "07-22" },
    { name: "Leo", start: "07-23", end: "08-22" },
    { name: "Virgo", start: "08-23", end: "09-22" },
    { name: "Libra", start: "09-23", end: "10-22" },
    { name: "Scorpio", start: "10-23", end: "11-21" },
    { name: "Sagittarius", start: "11-22", end: "12-21" },
    { name: "Capricorn", start: "12-22", end: "01-19" },
    { name: "Aquarius", start: "01-20", end: "02-18" },
    { name: "Pisces", start: "02-19", end: "03-20" },
  ]

  const month = Number.parseInt(birthDate.substring(5, 7))
  const day = Number.parseInt(birthDate.substring(8, 10))
  const birthDateFormatted = `${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`

  return (
    zodiacSigns.find((sign) => {
      const [startMonth, startDay] = sign.start.split("-").map(Number)
      const [endMonth, endDay] = sign.end.split("-").map(Number)

      const startDate = new Date(2024, startMonth - 1, startDay)
      const endDate = new Date(2024, endMonth - 1, endDay)
      const checkDate = new Date(2024, month - 1, day)

      if (startMonth <= endMonth) {
        return checkDate >= startDate && checkDate <= endDate
      } else {
        return checkDate >= startDate || checkDate <= endDate
      }
    })?.name || "Unknown"
  )
}

function getSimulatedAstronomyData() {
  return {
    sun: "Bright and shining",
    moon: "Full and luminous",
    planets: ["Venus", "Mars", "Jupiter"],
  }
}

function getSimulatedMusicData(birthDate: string) {
  const decade = Math.floor(Number.parseInt(birthDate.substring(0, 4)) / 10) * 10
  return {
    genre: "Pop",
    artist: "Simulated Artist",
    song: `Song from the ${decade}s`,
  }
}

function getSimulatedWeatherData() {
  return {
    temperature: 25,
    condition: "Sunny",
    forecast: "Clear skies ahead",
  }
}

function getSimulatedNewsData(birthDate: string, birthPlace: string) {
  return {
    headline: `Simulated News from ${birthPlace}`,
    article: `Interesting events happening on ${birthDate}`,
  }
}

function getSimulatedAstroReport(name: string, birthDate: string) {
  return {
    greeting: `Hello, ${name}!`,
    report: `Your simulated astro report for ${birthDate} is ready.`,
  }
}

