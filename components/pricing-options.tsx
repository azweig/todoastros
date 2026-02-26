"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckIcon, XIcon, MoonIcon, StarsIcon } from "lucide-react"
import { useLanguage } from "@/contexts/language-context"
import { LanguageSwitcher } from "./language-switcher"

export function PricingOptions() {
  const router = useRouter()
  const { t } = useLanguage()
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)

  const handleSelectPlan = (plan: string) => {
    setSelectedPlan(plan)

    // Store the selected plan in localStorage or context
    localStorage.setItem("selectedPlan", plan)

    // Navigate to the form page
    router.push("/form")
  }

  return (
    <div className="py-12 px-4">
      <div className="absolute top-4 right-4 z-20">
        <LanguageSwitcher />
      </div>

      <div className="text-center mb-12">
        <div className="flex justify-center mb-4">
          <div className="relative">
            <MoonIcon className="h-12 w-12 text-indigo-600 dark:text-indigo-400" />
            <StarsIcon className="h-6 w-6 text-yellow-500 absolute -top-1 -right-1" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-slate-800 dark:text-white mb-4">{t("pricing.title")}</h1>
        <p className="text-xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto">{t("pricing.subtitle")}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        {/* Free Plan */}
        <Card className="border-2 border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm hover:shadow-lg transition-all duration-300">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-bold">{t("pricing.free.title")}</CardTitle>
            <div className="text-4xl font-bold mt-4 mb-2 text-slate-800 dark:text-white">{t("pricing.free.price")}</div>
            <CardDescription>{t("pricing.free.desc")}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ul className="space-y-3">
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.basic.analysis")}</span>
              </li>
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.compatibility")}</span>
              </li>
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.general.predictions")}</span>
              </li>
              <li className="flex items-start">
                <XIcon className="h-5 w-5 text-slate-400 mr-2 flex-shrink-0 mt-0.5" />
                <span className="text-slate-500 dark:text-slate-400">{t("feature.no.exact.time")}</span>
              </li>
              <li className="flex items-start">
                <XIcon className="h-5 w-5 text-slate-400 mr-2 flex-shrink-0 mt-0.5" />
                <span className="text-slate-500 dark:text-slate-400">{t("feature.no.music")}</span>
              </li>
              <li className="flex items-start">
                <XIcon className="h-5 w-5 text-slate-400 mr-2 flex-shrink-0 mt-0.5" />
                <span className="text-slate-500 dark:text-slate-400">{t("feature.no.historical")}</span>
              </li>
              <li className="flex items-start">
                <XIcon className="h-5 w-5 text-slate-400 mr-2 flex-shrink-0 mt-0.5" />
                <span className="text-slate-500 dark:text-slate-400">{t("feature.no.weather")}</span>
              </li>
            </ul>
          </CardContent>
          <CardFooter>
            <Button
              onClick={() => handleSelectPlan("free")}
              className="w-full bg-slate-200 hover:bg-slate-300 text-slate-800"
            >
              {t("pricing.free.select")}
            </Button>
          </CardFooter>
        </Card>

        {/* Premium Plan */}
        <Card className="border-2 border-indigo-500 dark:border-indigo-400 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm hover:shadow-xl transition-all duration-300 relative">
          <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-indigo-600 text-white px-4 py-1 rounded-full text-sm font-medium">
            {t("pricing.recommended")}
          </div>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-bold">{t("pricing.premium.title")}</CardTitle>
            <div className="text-4xl font-bold mt-4 mb-2 text-indigo-600 dark:text-indigo-400">
              {t("pricing.premium.price")}
            </div>
            <CardDescription>{t("pricing.premium.desc")}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ul className="space-y-3">
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.detailed.analysis")}</span>
              </li>
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.houses")}</span>
              </li>
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.planetary")}</span>
              </li>
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.exact.time")}</span>
              </li>
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.music")}</span>
              </li>
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.historical")}</span>
              </li>
              <li className="flex items-start">
                <CheckIcon className="h-5 w-5 text-green-500 mr-2 flex-shrink-0 mt-0.5" />
                <span>{t("feature.weather")}</span>
              </li>
            </ul>
          </CardContent>
          <CardFooter>
            <Button
              onClick={() => handleSelectPlan("premium")}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white"
            >
              {t("pricing.premium.select")}
            </Button>
          </CardFooter>
        </Card>
      </div>

      <div className="text-center mt-12">
        <Link href="/">
          <Button variant="link" className="text-slate-600 dark:text-slate-300">
            {t("pricing.back")}
          </Button>
        </Link>
      </div>
    </div>
  )
}

