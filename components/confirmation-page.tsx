"use client"

import { useEffect, useState, Suspense } from "react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { CheckCircle, MoonIcon, SunIcon, SparklesIcon } from "lucide-react"
import { useLanguage } from "@/contexts/language-context"
import { LanguageSwitcher } from "./language-switcher"

// Componente interno que usa useSearchParams
function ConfirmationContent() {
  const { t } = useLanguage()
  const [progress, setProgress] = useState(0)
  const [selectedPlan, setSelectedPlan] = useState<string>("free")
  const searchParams = useSearchParams()
  const chartUrl = searchParams.get("chartUrl")

  useEffect(() => {
    // Get the selected plan from localStorage
    const plan = localStorage.getItem("selectedPlan")
    if (plan) {
      setSelectedPlan(plan)
    }

    const timer = setTimeout(() => {
      setProgress(100)
    }, 3000)

    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress >= 100) {
          clearInterval(interval)
          return 100
        }
        return prevProgress + 5
      })
    }, 150)

    return () => {
      clearTimeout(timer)
      clearInterval(interval)
    }
  }, [])

  return (
    <Card className="w-full max-w-md shadow-lg border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm">
      <CardHeader className="space-y-1 text-center">
        <div className="flex justify-center mb-2">
          <div className="relative">
            <MoonIcon className="h-10 w-10 text-indigo-600 dark:text-indigo-400" />
            <SunIcon className="h-5 w-5 text-yellow-500 absolute -top-1 -right-1" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">
          {selectedPlan === "premium" ? t("confirm.premium.title") : t("confirm.free.title")}
        </CardTitle>
        <CardDescription>
          {selectedPlan === "premium" ? t("confirm.premium.desc") : t("confirm.free.desc")}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <div className="flex justify-between text-sm font-medium">
            <span>{t("confirm.progress")}</span>
            <span>{progress}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {progress === 100 ? (
          <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800 flex items-center space-x-3">
            <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400 flex-shrink-0" />
            <div className="text-green-700 dark:text-green-300 text-sm">
              {selectedPlan === "premium" ? t("confirm.premium.success") : t("confirm.free.success")}
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="animate-pulse space-y-2">
              <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4"></div>
              <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/2"></div>
            </div>
          </div>
        )}

        <div className="text-center text-sm text-slate-500 dark:text-slate-400">
          <p>{selectedPlan === "premium" ? t("confirm.premium.processing") : t("confirm.free.processing")}</p>
        </div>

        {selectedPlan === "premium" && (
          <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg border border-indigo-100 dark:border-indigo-800">
            <h3 className="font-medium text-indigo-800 dark:text-indigo-300 mb-2 flex items-center">
              <SparklesIcon className="h-4 w-4 mr-2" />
              {t("confirm.premium.benefits")}
            </h3>
            <ul className="text-sm space-y-1 text-slate-700 dark:text-slate-300">
              <li>• {t("feature.detailed.analysis")}</li>
              <li>• {t("feature.music")}</li>
              <li>• {t("feature.historical")}</li>
              <li>• {t("feature.weather")}</li>
              <li>• {t("feature.planetary")}</li>
            </ul>
          </div>
        )}

        {chartUrl && progress === 100 && (
          <div className="mt-4">
            <Button className="w-full" variant="outline" onClick={() => window.open(chartUrl, "_blank")}>
              {t("confirm.view.chart")}
            </Button>
          </div>
        )}
      </CardContent>
      <CardFooter className="flex justify-center">
        <Link href="/">
          <Button variant="outline">{t("confirm.back")}</Button>
        </Link>
      </CardFooter>
    </Card>
  )
}

// Componente principal que envuelve el contenido en Suspense
export function ConfirmationPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center p-4">
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="stars-bg"></div>
      </div>

      <div className="absolute top-4 right-4 z-20">
        <LanguageSwitcher />
      </div>

      <Suspense
        fallback={
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
        }
      >
        <ConfirmationContent />
      </Suspense>
    </div>
  )
}

