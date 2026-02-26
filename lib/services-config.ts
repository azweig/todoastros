// Configuración de los servicios de backend
// Estas URLs solo se utilizarán en el servidor, nunca en el cliente
export const SERVICES = {
  AGGREGATOR: process.env.ASTRO_SERVICE_AGGREGATOR || "http://127.0.0.1:5000/generate_complete_json",
  ZODIAC: process.env.ASTRO_SERVICE_ZODIAC || "http://127.0.0.1:5001/zodiac",
  MUSIC: process.env.ASTRO_SERVICE_MUSIC || "http://127.0.0.1:5002/music",
  ASTRONOMY: process.env.ASTRO_SERVICE_ASTRONOMY || "http://127.0.0.1:5003/astronomy",
  WEATHER: process.env.ASTRO_SERVICE_WEATHER || "http://127.0.0.1:5004/weather",
  NEWS: process.env.ASTRO_SERVICE_NEWS || "http://127.0.0.1:5007/news",
  ASTRO_REPORT: process.env.ASTRO_SERVICE_REPORT || "http://127.0.0.1:5006/astro_report",
  OPENAI: process.env.ASTRO_SERVICE_OPENAI || "http://127.0.0.1:5010/openai",
}

// Función para verificar si estamos en modo desarrollo
export const isDevelopment = () => {
  return process.env.NODE_ENV === "development"
}

// Función para verificar si los servicios están disponibles
// Esta función solo se ejecutará en el servidor
export const checkServiceAvailability = async (serviceUrl: string): Promise<boolean> => {
  if (isDevelopment()) {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 1000)

      const response = await fetch(serviceUrl, {
        method: "HEAD",
        signal: controller.signal,
      })

      clearTimeout(timeoutId)
      return response.ok
    } catch (error) {
      console.warn(`Service ${serviceUrl} is not available:`, error)
      return false
    }
  }
  return false
}

