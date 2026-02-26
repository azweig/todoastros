"use server"

import { redirect } from "next/navigation"
import { generateAstralChart } from "@/lib/chart-generator"

interface ChartData {
  name: string
  email: string
  birthDate: string
  birthTime?: string
  birthPlace?: string
  plan: "free" | "premium"
}

export async function generateChart(formData: FormData) {
  try {
    const data: ChartData = {
      name: formData.get("fullName") as string,
      email: formData.get("email") as string,
      birthDate: formData.get("birthDate") as string,
      plan: formData.get("plan") as "free" | "premium",
    }

    if (data.plan === "premium") {
      data.birthTime = formData.get("birthTime") as string
      data.birthPlace = formData.get("birthPlace") as string
    }

    // Generar la carta astral
    const chartUrl = await generateAstralChart(data)

    // Redirigir a la página de visualización de la carta
    redirect(chartUrl)
  } catch (error) {
    console.error("Error generating chart:", error)
    // Redirigir a una página de error
    redirect("/error?message=Failed+to+generate+chart")
  }
}

