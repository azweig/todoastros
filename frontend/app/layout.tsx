import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { ThemeProvider } from "@/components/theme-provider"
import { ClientLanguageProvider } from "@/components/client-language-provider"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "AstroFuturo - Descubre tu destino en las estrellas",
  description: "Cartas astrales personalizadas con inteligencia artificial",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
          <ClientLanguageProvider>{children}</ClientLanguageProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}



import './globals.css'