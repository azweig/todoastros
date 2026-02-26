// Mock de Redis para desarrollo
interface RedisStore {
  [key: string]: any
}

// Almacenamiento en memoria para desarrollo
const store: RedisStore = {}

export async function storeChartRequest(sessionId: string, data: any): Promise<void> {
  store[sessionId] = data
  console.log("Stored chart request for session:", sessionId)
  return Promise.resolve()
}

export async function getStoredChartRequest(sessionId: string): Promise<any> {
  const request = store[sessionId]

  if (!request) {
    throw new Error(`No chart request found for session ID: ${sessionId}`)
  }

  return Promise.resolve(request)
}

