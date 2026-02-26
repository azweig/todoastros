"use client"

import { useSearchParams } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertTriangle } from "lucide-react"
import { useLanguage } from "@/contexts/language-context"
import { Suspense } from "react"

// Componente interno que usa useSearchParams
function ErrorContent() {
  const { t } = useLanguage()
  const searchParams = useSearchParams()
  const errorMessage = searchParams.get("message") || t("error.default")

  return (
    <Card className="w-full max-w-md shadow-lg">
      <CardHeader className="text-center">
        <div className="flex justify-center mb-4">
          <AlertTriangle className="h-12 w-12 text-red-500" />
        </div>
        <CardTitle className="text-2xl font-bold text-red-600">{t("error.title")}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-center">{decodeURIComponent(errorMessage)}</p>
      </CardContent>
      <CardFooter className="flex justify-center">
        <Link href="/">
          <Button>{t("error.back")}</Button>
        </Link>
      </CardFooter>
    </Card>
  )
}

// Componente principal que envuelve el contenido en Suspense
export default function ErrorPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center p-4">
      <Suspense
        fallback={
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-500"></div>
          </div>
        }
      >
        <ErrorContent />
      </Suspense>
    </div>
  )
}

