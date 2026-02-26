import { redirect } from "next/navigation"
import { getStoredChartRequest } from "@/lib/redis"
import { generateCompleteAstrology } from "@/lib/services/aggregator-service"

export async function GET(request: Request) {
  const url = new URL(request.url)
  const sessionId = url.searchParams.get("session_id")

  if (!sessionId) {
    return redirect("/error?message=Session+ID+is+required")
  }

  try {
    // Recuperar los datos de la carta almacenados
    const chartData = await getStoredChartRequest(sessionId)

    // Generar la carta astral
    const astrologyData = await generateCompleteAstrology({
      name: chartData.name,
      birthDate: chartData.birthDate,
      birthTime: chartData.birthTime,
      birthPlace: chartData.birthPlace,
      plan: chartData.plan,
    })

    // Codificar los datos para pasarlos a la URL
    const chartDataEncoded = encodeURIComponent(
      JSON.stringify({
        chartData: chartData,
        astrologyData,
      }),
    )

    // Redirigir a la página de visualización de la carta
    return redirect(`/view-chart?data=${chartDataEncoded}`)
  } catch (error) {
    console.error("Error processing payment success:", error)
    return redirect("/error?message=Error+processing+payment")
  }
}

