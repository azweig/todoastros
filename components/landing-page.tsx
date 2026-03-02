"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { MoonIcon, StarsIcon } from "lucide-react"
import { useLanguage } from "@/contexts/language-context"
// Cambiamos la importación para usar la ruta relativa
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
    // Reset typing when language changes
    setDisplayText("")
    setIsDeleting(false)
    setCurrentPhraseIndex(0)
  }, [language])

  useEffect(() => {
    const phrases = motivationalPhrases[language]
    const currentPhrase = phrases[currentPhraseIndex]

    const timer = setTimeout(() => {
      if (!isDeleting) {
        // Typing effect
        setDisplayText(currentPhrase.substring(0, displayText.length + 1))
        setTypingSpeed(150)

        // If we've typed the full phrase, start deleting after a pause
        if (displayText === currentPhrase) {
          setTypingSpeed(2000) // Pause before deleting
          setIsDeleting(true)
        }
      } else {
        // Deleting effect
        setDisplayText(currentPhrase.substring(0, displayText.length - 1))
        setTypingSpeed(50)

        // If we've deleted the full phrase, move to the next one
        if (displayText === "") {
          setIsDeleting(false)
          setCurrentPhraseIndex((prevIndex) => (prevIndex + 1) % phrases.length)
        }
      }
    }, typingSpeed)

    return () => clearTimeout(timer)
  }, [displayText, currentPhraseIndex, isDeleting, typingSpeed, language])

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-screen text-center">
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
          <div className="stars-bg"></div>
        </div>

        <div className="absolute top-4 right-4 z-20">
          <LanguageSwitcher />
        </div>

        <div className="relative z-10 space-y-8 max-w-3xl">
          <div className="flex justify-center mb-8">
            <div className="relative">
              <MoonIcon className="h-16 w-16 text-indigo-600 dark:text-indigo-400" />
              <StarsIcon className="h-8 w-8 text-yellow-500 absolute -top-2 -right-2" />
            </div>
          </div>

          <h1 className="text-5xl md:text-6xl font-bold text-slate-800 dark:text-white">{t("app.title")}</h1>

          <h2 className="text-3xl md:text-4xl font-semibold text-slate-700 dark:text-slate-200">{t("app.subtitle")}</h2>

          <div className="h-20 flex items-center justify-center">
            <p className="text-xl text-slate-600 dark:text-slate-300 italic transition-opacity duration-500">
              {displayText}
              <span className="animate-pulse">|</span>
            </p>
          </div>

          <div className="max-w-2xl mx-auto">
            <p className="text-lg text-slate-600 dark:text-slate-300 mb-6">{t("app.description")}</p>
          </div>

          <div className="pt-8">
            <Link href="/pricing">
              <Button
                size="lg"
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-6 text-lg rounded-full transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                {t("app.cta")}
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="bg-white/30 dark:bg-slate-800/30 backdrop-blur-sm p-6 rounded-lg">
              <h3 className="text-xl font-semibold mb-2 text-indigo-700 dark:text-indigo-400">
                {t("feature.personalized")}
              </h3>
              <p className="text-slate-600 dark:text-slate-300">{t("feature.personalized.desc")}</p>
            </div>
            <div className="bg-white/30 dark:bg-slate-800/30 backdrop-blur-sm p-6 rounded-lg">
              <h3 className="text-xl font-semibold mb-2 text-indigo-700 dark:text-indigo-400">{t("feature.cosmic")}</h3>
              <p className="text-slate-600 dark:text-slate-300">{t("feature.cosmic.desc")}</p>
            </div>
            <div className="bg-white/30 dark:bg-slate-800/30 backdrop-blur-sm p-6 rounded-lg">
              <h3 className="text-xl font-semibold mb-2 text-indigo-700 dark:text-indigo-400">
                {t("feature.spiritual")}
              </h3>
              <p className="text-slate-600 dark:text-slate-300">{t("feature.spiritual.desc")}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}

