// Simulación de base de datos para desarrollo
interface ChartRequest {
  name: string
  email: string
  birthDate: string
  birthTime?: string
  birthPlace?: string
  plan: string
  sessionId?: string
}

// Almacenamiento en memoria para desarrollo
const chartRequests: Record<string, ChartRequest> = {}

export async function storeChartRequest(data: ChartRequest): Promise<void> {
  if (!data.sessionId) {
    throw new Error("Session ID is required")
  }

  chartRequests[data.sessionId] = data
  console.log("Stored chart request:", data)
  return Promise.resolve()
}

export async function getStoredChartRequest(sessionId: string): Promise<ChartRequest> {
  const request = chartRequests[sessionId]

  if (!request) {
    throw new Error(`No chart request found for session ID: ${sessionId}`)
  }

  return Promise.resolve(request)
}

