"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Moon, Sparkles, Star, Sun } from "lucide-react"
import { useLanguage } from "@/contexts/language-context"
import { LanguageSwitcher } from "../components/language-switcher"

export function LandingPage() {
  const { t, language } = useLanguage()
  const [displayText, setDisplayText] = useState("")
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0)
  const [isDeleting, setIsDeleting] = useState(false)
  const [typingSpeed, setTypingSpeed] = useState(150)

  const motivationalPhrases = {
    es: [
      "Tu futuro está escrito en las estrellas",
      "La sabiduría celestial guía tu camino",
      "Descubre los secretos que el universo tiene para ti",
      "Las estrellas revelan tu verdadero potencial",
      "Conecta con la energía cósmica que te rodea",
    ],
    en: [
      "Your future is written in the stars",
      "Celestial wisdom guides your path",
      "Discover the secrets the universe has for you",
      "The stars reveal your true potential",
      "Connect with the cosmic energy around you",
    ],
  }

  useEffect(() => {
    setDisplayText("")
    setIsDeleting(false)
    setCurrentPhraseIndex(0)
  }, [language])

  useEffect(() => {
    const phrases = motivationalPhrases[language]
    const currentPhrase = phrases[currentPhraseIndex]

    const timer = setTimeout(() => {
      if (!isDeleting) {
        setDisplayText(currentPhrase.substring(0, displayText.length + 1))
        setTypingSpeed(150)

        if (displayText === currentPhrase) {
          setTypingSpeed(2000)
          setIsDeleting(true)
        }
      } else {
        setDisplayText(currentPhrase.substring(0, displayText.length - 1))
        setTypingSpeed(50)

        if (displayText === "") {
          setIsDeleting(false)
          setCurrentPhraseIndex((prevIndex) => (prevIndex + 1) % phrases.length)
        }
      }
    }, typingSpeed)

    return () => clearTimeout(timer)
  }, [displayText, currentPhraseIndex, isDeleting, typingSpeed, language])

  return (
    <main className="min-h-screen hero-gradient relative overflow-hidden">
      {/* Animated stars background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 animate-float" style={{ animationDelay: '0s' }}>
          <Star className="h-4 w-4 text-gold/40" fill="currentColor" />
        </div>
        <div className="absolute top-40 right-20 animate-float" style={{ animationDelay: '0.5s' }}>
          <Sparkles className="h-6 w-6 text-gold/30" />
        </div>
        <div className="absolute top-60 left-1/4 animate-float" style={{ animationDelay: '1s' }}>
          <Star className="h-3 w-3 text-gold/50" fill="currentColor" />
        </div>
        <div className="absolute bottom-40 right-1/3 animate-float" style={{ animationDelay: '1.5s' }}>
          <Star className="h-5 w-5 text-gold/35" fill="currentColor" />
        </div>
        <div className="absolute bottom-20 left-1/3 animate-float" style={{ animationDelay: '2s' }}>
          <Sparkles className="h-4 w-4 text-gold/40" />
        </div>
      </div>

      {/* Language switcher */}
      <div className="absolute top-6 right-6 z-20">
        <LanguageSwitcher />
      </div>

      <div className="container mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-screen text-center relative z-10">
        <div className="space-y-8 max-w-4xl">
          {/* Logo/Icon */}
          <div className="flex justify-center mb-8">
            <div className="relative group">
              <div className="absolute inset-0 bg-gold/20 rounded-full blur-xl group-hover:blur-2xl transition-all duration-500" />
              <div className="relative bg-gradient-to-br from-primary-dark to-primary-navy p-6 rounded-full border border-gold/30 shadow-gold">
                <Moon className="h-14 w-14 text-gold" />
                <Sparkles className="h-6 w-6 text-gold absolute -top-1 -right-1 animate-pulse" />
              </div>
            </div>
          </div>

          {/* Title */}
          <h1 className="font-display text-5xl md:text-7xl font-bold text-gradient tracking-tight">
            {t("app.title") || "TodoAstros"}
          </h1>

          {/* Subtitle */}
          <h2 className="font-display text-2xl md:text-3xl font-medium text-white/90">
            {t("app.subtitle") || "Tu Cosmograma Natal Completo"}
          </h2>

          {/* Typing animation */}
          <div className="h-16 flex items-center justify-center">
            <p className="text-lg md:text-xl text-gold/80 italic font-light">
              {displayText}
              <span className="animate-pulse text-gold">|</span>
            </p>
          </div>

          {/* Description */}
          <div className="max-w-2xl mx-auto">
            <p className="text-lg text-white/70 leading-relaxed">
              {t("app.description") || "Descubre los secretos de tu carta astral con un análisis profundo de tu personalidad, destino y potencial cósmico."}
            </p>
          </div>

          {/* CTA Button */}
          <div className="pt-8">
            <Link href="/pricing">
              <Button
                size="lg"
                className="btn-gold text-lg px-10 py-6 rounded-full font-semibold"
              >
                <Sparkles className="mr-2 h-5 w-5" />
                {t("app.cta") || "Obtener Mi Carta Astral"}
              </Button>
            </Link>
          </div>

          {/* Divider */}
          <div className="divider-star pt-8">
            <span>✦</span>
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="card-premium group cursor-pointer bg-white/5 backdrop-blur-sm border-gold/20 hover:border-gold/40">
              <div className="flex justify-center mb-4">
                <div className="p-3 rounded-full bg-zodiac-fire/10 group-hover:bg-zodiac-fire/20 transition-colors">
                  <Sun className="h-8 w-8 text-zodiac-fire" />
                </div>
              </div>
              <h3 className="text-xl font-display font-semibold mb-2 text-gold">
                {t("feature.personalized") || "Carta Personalizada"}
              </h3>
              <p className="text-white/60 text-sm">
                {t("feature.personalized.desc") || "Análisis único basado en tu fecha, hora y lugar de nacimiento exactos."}
              </p>
            </div>

            <div className="card-premium group cursor-pointer bg-white/5 backdrop-blur-sm border-gold/20 hover:border-gold/40">
              <div className="flex justify-center mb-4">
                <div className="p-3 rounded-full bg-zodiac-water/10 group-hover:bg-zodiac-water/20 transition-colors">
                  <Moon className="h-8 w-8 text-zodiac-water" />
                </div>
              </div>
              <h3 className="text-xl font-display font-semibold mb-2 text-gold">
                {t("feature.cosmic") || "Numerología Profunda"}
              </h3>
              <p className="text-white/60 text-sm">
                {t("feature.cosmic.desc") || "Descubre tu número de vida, destino y el significado oculto de tu nombre."}
              </p>
            </div>

            <div className="card-premium group cursor-pointer bg-white/5 backdrop-blur-sm border-gold/20 hover:border-gold/40">
              <div className="flex justify-center mb-4">
                <div className="p-3 rounded-full bg-zodiac-air/10 group-hover:bg-zodiac-air/20 transition-colors">
                  <Sparkles className="h-8 w-8 text-zodiac-air" />
                </div>
              </div>
              <h3 className="text-xl font-display font-semibold mb-2 text-gold">
                {t("feature.spiritual") || "PDF Premium"}
              </h3>
              <p className="text-white/60 text-sm">
                {t("feature.spiritual.desc") || "Recibe un documento profesional con gráficos y análisis detallado."}
              </p>
            </div>
          </div>

          {/* Trust badges */}
          <div className="flex flex-wrap justify-center gap-6 mt-12 text-white/40 text-sm">
            <div className="flex items-center gap-2">
              <Star className="h-4 w-4 text-gold/60" fill="currentColor" />
              <span>+10,000 cartas generadas</span>
            </div>
            <div className="flex items-center gap-2">
              <Star className="h-4 w-4 text-gold/60" fill="currentColor" />
              <span>Astrólogos certificados</span>
            </div>
            <div className="flex items-center gap-2">
              <Star className="h-4 w-4 text-gold/60" fill="currentColor" />
              <span>Entrega inmediata</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="absolute bottom-0 w-full py-4 text-center text-white/30 text-sm">
        <p>© 2024-2026 TodoAstros. Todos los derechos reservados.</p>
      </footer>
    </main>
  )
}
