// Servicio de clima integrado en Next.js

interface WeatherResponse {
  temperature: number
  description: string
}

export function getWeatherData(dateOfBirth: string, cityOfBirth: string): WeatherResponse {
  // Usar la fecha y ciudad como semilla para generar datos "deterministas"
  const dateSeed = new Date(dateOfBirth).getTime()
  const citySeed = cityOfBirth.split("").reduce((acc, char) => acc + char.charCodeAt(0), 0)
  const combinedSeed = (dateSeed + citySeed) % 100000

  // Generar temperatura basada en la semilla (entre 5°C y 35°C)
  const temperature = 5 + (combinedSeed % 30)

  // Determinar descripción del clima basada en la temperatura
  let description = "Desconocido"
  if (temperature < 10) {
    description = "Frío"
  } else if (temperature < 15) {
    description = "Fresco"
  } else if (temperature < 20) {
    description = "Templado"
  } else if (temperature < 25) {
    description = "Cálido"
  } else if (temperature < 30) {
    description = "Caluroso"
  } else {
    description = "Muy caluroso"
  }

  // Añadir condiciones climáticas basadas en el resto de la semilla
  const conditions = combinedSeed % 5
  if (conditions === 0) {
    description += " y soleado"
  } else if (conditions === 1) {
    description += " y parcialmente nublado"
  } else if (conditions === 2) {
    description += " y nublado"
  } else if (conditions === 3) {
    description += " con lluvia ligera"
  } else {
    description += " con tormentas"
  }

  return {
    temperature,
    description,
  }
}

