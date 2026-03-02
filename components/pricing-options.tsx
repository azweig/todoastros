"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Check, X, Moon, Sparkles, Star, Crown, ArrowLeft } from "lucide-react"
import { useLanguage } from "@/contexts/language-context"
import { LanguageSwitcher } from "./language-switcher"

export function PricingOptions() {
  const router = useRouter()
  const { t } = useLanguage()
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)

  const handleSelectPlan = (plan: string) => {
    setSelectedPlan(plan)
    localStorage.setItem("selectedPlan", plan)
    router.push("/form")
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted py-12 px-4 relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-20 left-10 animate-float opacity-20">
        <Star className="h-6 w-6 text-gold" fill="currentColor" />
      </div>
      <div className="absolute top-40 right-20 animate-float opacity-20" style={{ animationDelay: '1s' }}>
        <Sparkles className="h-8 w-8 text-gold" />
      </div>
      <div className="absolute bottom-40 left-1/4 animate-float opacity-20" style={{ animationDelay: '2s' }}>
        <Star className="h-4 w-4 text-gold" fill="currentColor" />
      </div>

      {/* Language switcher */}
      <div className="absolute top-6 right-6 z-20">
        <LanguageSwitcher />
      </div>

      {/* Back button */}
      <div className="absolute top-6 left-6">
        <Link href="/">
          <Button variant="ghost" className="text-foreground/70 hover:text-foreground">
            <ArrowLeft className="h-4 w-4 mr-2" />
            {t("pricing.back") || "Volver"}
          </Button>
        </Link>
      </div>

      <div className="max-w-6xl mx-auto pt-8">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-gold/20 rounded-full blur-xl" />
              <div className="relative bg-gradient-to-br from-primary to-secondary p-4 rounded-full border border-gold/30 shadow-gold">
                <Moon className="h-10 w-10 text-gold" />
              </div>
            </div>
          </div>
          <h1 className="font-display text-4xl md:text-5xl font-bold text-foreground mb-4">
            {t("pricing.title") || "Elige tu Carta Astral"}
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            {t("pricing.subtitle") || "Descubre los secretos que el universo tiene guardados para ti"}
          </p>
        </div>

        {/* Pricing cards */}
        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Free Plan */}
          <Card className="pricing-card border-border/50 hover:border-gold/30 transition-all duration-300 group">
            <CardHeader className="text-center pb-2">
              <div className="flex justify-center mb-4">
                <div className="p-3 rounded-full bg-muted group-hover:bg-gold/10 transition-colors">
                  <Star className="h-8 w-8 text-muted-foreground group-hover:text-gold transition-colors" />
                </div>
              </div>
              <CardTitle className="font-display text-2xl font-bold">
                {t("pricing.free.title") || "Carta Básica"}
              </CardTitle>
              <div className="mt-4 mb-2">
                <span className="text-5xl font-bold text-foreground">
                  {t("pricing.free.price") || "Gratis"}
                </span>
              </div>
              <CardDescription className="text-muted-foreground">
                {t("pricing.free.desc") || "Análisis introductorio de tu signo solar"}
              </CardDescription>
            </CardHeader>
            
            <CardContent className="pt-6">
              <ul className="space-y-4">
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-green-500" />
                  </div>
                  <span className="text-foreground/80">{t("feature.basic.analysis") || "Análisis de signo solar"}</span>
                </li>
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-green-500" />
                  </div>
                  <span className="text-foreground/80">{t("feature.compatibility") || "Compatibilidad básica"}</span>
                </li>
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-green-500" />
                  </div>
                  <span className="text-foreground/80">{t("feature.general.predictions") || "Predicciones generales"}</span>
                </li>
                <li className="flex items-start opacity-50">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <X className="h-5 w-5 text-muted-foreground" />
                  </div>
                  <span className="text-muted-foreground">{t("feature.no.exact.time") || "Sin hora exacta de nacimiento"}</span>
                </li>
                <li className="flex items-start opacity-50">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <X className="h-5 w-5 text-muted-foreground" />
                  </div>
                  <span className="text-muted-foreground">{t("feature.no.music") || "Sin música de tu época"}</span>
                </li>
                <li className="flex items-start opacity-50">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <X className="h-5 w-5 text-muted-foreground" />
                  </div>
                  <span className="text-muted-foreground">{t("feature.no.historical") || "Sin eventos históricos"}</span>
                </li>
              </ul>
            </CardContent>
            
            <CardFooter className="pt-6">
              <Button
                onClick={() => handleSelectPlan("free")}
                variant="outline"
                className="w-full py-6 text-lg border-2 hover:border-gold hover:bg-gold/5 transition-all"
              >
                {t("pricing.free.select") || "Comenzar Gratis"}
              </Button>
            </CardFooter>
          </Card>

          {/* Premium Plan */}
          <Card className="pricing-card featured relative overflow-hidden">
            {/* Recommended badge */}
            <div className="absolute -top-px left-1/2 transform -translate-x-1/2">
              <div className="bg-gradient-gold text-primary-dark px-6 py-1.5 rounded-b-lg text-sm font-semibold flex items-center gap-2 shadow-gold">
                <Crown className="h-4 w-4" />
                {t("pricing.recommended") || "Recomendado"}
              </div>
            </div>
            
            <CardHeader className="text-center pb-2 pt-10">
              <div className="flex justify-center mb-4">
                <div className="p-3 rounded-full bg-gold/20">
                  <Sparkles className="h-8 w-8 text-gold" />
                </div>
              </div>
              <CardTitle className="font-display text-2xl font-bold text-gradient">
                {t("pricing.premium.title") || "Carta Premium"}
              </CardTitle>
              <div className="mt-4 mb-2">
                <span className="text-5xl font-bold text-foreground">
                  {t("pricing.premium.price") || "$9.99"}
                </span>
                <span className="text-muted-foreground ml-2">USD</span>
              </div>
              <CardDescription className="text-muted-foreground">
                {t("pricing.premium.desc") || "Cosmograma natal completo con numerología"}
              </CardDescription>
            </CardHeader>
            
            <CardContent className="pt-6">
              <ul className="space-y-4">
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-gold" />
                  </div>
                  <span className="text-foreground/90 font-medium">{t("feature.detailed.analysis") || "Análisis detallado Sol, Luna y Ascendente"}</span>
                </li>
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-gold" />
                  </div>
                  <span className="text-foreground/90 font-medium">{t("feature.houses") || "12 casas astrológicas completas"}</span>
                </li>
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-gold" />
                  </div>
                  <span className="text-foreground/90 font-medium">{t("feature.planetary") || "Posiciones planetarias exactas"}</span>
                </li>
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-gold" />
                  </div>
                  <span className="text-foreground/90 font-medium">{t("feature.exact.time") || "Cálculo con hora exacta"}</span>
                </li>
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-gold" />
                  </div>
                  <span className="text-foreground/90 font-medium">{t("feature.music") || "Música popular de tu nacimiento"}</span>
                </li>
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-gold" />
                  </div>
                  <span className="text-foreground/90 font-medium">{t("feature.numerology") || "Numerología completa del nombre"}</span>
                </li>
                <li className="flex items-start">
                  <div className="flex-shrink-0 mt-0.5 mr-3">
                    <Check className="h-5 w-5 text-gold" />
                  </div>
                  <span className="text-foreground/90 font-medium">{t("feature.pdf") || "PDF profesional descargable"}</span>
                </li>
              </ul>
            </CardContent>
            
            <CardFooter className="pt-6">
              <Button
                onClick={() => handleSelectPlan("premium")}
                className="w-full py-6 text-lg btn-gold font-semibold"
              >
                <Sparkles className="mr-2 h-5 w-5" />
                {t("pricing.premium.select") || "Obtener Premium"}
              </Button>
            </CardFooter>
          </Card>
        </div>

        {/* Trust indicators */}
        <div className="flex flex-wrap justify-center gap-8 mt-16 text-muted-foreground text-sm">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-full bg-green-500/10">
              <Check className="h-4 w-4 text-green-500" />
            </div>
            <span>Pago seguro SSL</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-full bg-green-500/10">
              <Check className="h-4 w-4 text-green-500" />
            </div>
            <span>Entrega inmediata</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-full bg-green-500/10">
              <Check className="h-4 w-4 text-green-500" />
            </div>
            <span>Garantía de satisfacción</span>
          </div>
        </div>

        {/* Footer quote */}
        <div className="text-center mt-16">
          <p className="text-muted-foreground italic">
            "Los astros no obligan, pero sí inclinan. Tu voluntad es el timón."
          </p>
        </div>
      </div>
    </div>
  )
}
