import type { NextRequest } from "next/server"
import Stripe from "stripe"
import { Resend } from "resend"
import { getStoredChartRequest } from "@/lib/redis"
import { generateCompleteAstrology } from "@/lib/services/aggregator-service"

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || "", {
  apiVersion: "2023-10-16",
})
const resend = new Resend(process.env.RESEND_API_KEY)

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const sessionId = searchParams.get("session_id")

  if (!sessionId) {
    return new Response("Session ID is required", { status: 400 })
  }

  try {
    // Verificar si el pago fue exitoso
    const session = await stripe.checkout.sessions.retrieve(sessionId)
    if (session.payment_status !== "paid") {
      throw new Error("Payment not completed")
    }

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

    // Enviar email con la carta
    if (chartData.email) {
      await resend.emails.send({
        from: "AstroFuturo <charts@astrofuturo.com>",
        to: chartData.email,
        subject: "Your Premium Astral Chart is Ready! 🌟",
        html: `
          <h1>Hello ${chartData.name}!</h1>
          <p>Your premium astral chart is ready. Click the link below to view it:</p>
          <a href="${process.env.NEXT_PUBLIC_BASE_URL}/view-chart?data=${chartDataEncoded}">View Your Premium Astral Chart</a>
        `,
      })
    }

    // Redirigir a la página de visualización de la carta
    return Response.redirect(`${process.env.NEXT_PUBLIC_BASE_URL}/view-chart?data=${chartDataEncoded}`)
  } catch (error) {
    console.error("Error processing payment success:", error)
    return new Response("Error processing payment", { status: 500 })
  }
}

