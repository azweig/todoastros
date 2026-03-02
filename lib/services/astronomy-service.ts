// Servicio de astronomía integrado en Next.js

interface PlanetaryPosition {
  planet: string
  ra: string
  dec: string
}

interface AstronomyResponse {
  moon_phase: string
  planetary_positions: PlanetaryPosition[]
}

export function getAstronomicalData(dateOfBirth: string): AstronomyResponse {
  // Simulación de fase lunar basada en el día del mes
  const day = Number.parseInt(dateOfBirth.split("-")[2])
  let moonPhase = "Luna Nueva"

  if (day < 8) {
    moonPhase = "Luna Nueva"
  } else if (day < 15) {
    moonPhase = "Cuarto Creciente"
  } else if (day < 22) {
    moonPhase = "Luna Llena"
  } else {
    moonPhase = "Cuarto Menguante"
  }

  // Simulación de posiciones planetarias
  const planets = ["Sol", "Luna", "Mercurio", "Venus", "Marte", "Júpiter", "Saturno", "Urano", "Neptuno"]
  const planetaryPositions = planets.map((planet) => {
    // Usar el nombre del planeta como semilla para generar posiciones "deterministas"
    const seed = planet.split("").reduce((acc, char) => acc + char.charCodeAt(0), 0)
    const dateValue = new Date(dateOfBirth).getTime()
    const combinedSeed = seed + dateValue

    // Generar valores basados en la semilla
    const ra = `${combinedSeed % 24}h ${combinedSeed % 60}m`
    const dec = `${combinedSeed % 90}° ${combinedSeed % 60}'`

    return {
      planet,
      ra,
      dec,
    }
  })

  return {
    moon_phase: moonPhase,
    planetary_positions: planetaryPositions,
  }
}

