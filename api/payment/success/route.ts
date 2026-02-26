import type { NextRequest } from "next/server"
import Stripe from "stripe"
import { generateAstralChart } from "@/lib/astrology"
import { Resend } from "resend"
import { getStoredChartRequest } from "@/lib/redis"

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
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
    // Verify the payment was successful
    const session = await stripe.checkout.sessions.retrieve(sessionId)
    if (session.payment_status !== "paid") {
      throw new Error("Payment not completed")
    }

    // Retrieve the stored chart request data
    const chartData = await getStoredChartRequest(sessionId)

    // Generate the chart
    const chartUrl = await generateAstralChart(chartData)

    // Send email with the chart
    await resend.emails.send({
      from: "AstroFuturo <charts@astrofuturo.com>",
      to: chartData.email,
      subject: "Your Premium Astral Chart is Ready! 🌟",
      html: `
        <h1>Hello ${chartData.name}!</h1>
        <p>Your premium astral chart is ready. Click the link below to view it:</p>
        <a href="${chartUrl}">View Your Premium Astral Chart</a>
      `,
    })

    // Redirect to confirmation page
    return Response.redirect(`${process.env.NEXT_PUBLIC_BASE_URL}/confirmation`)
  } catch (error) {
    console.error("Error processing payment success:", error)
    return new Response("Error processing payment", { status: 500 })
  }
}

