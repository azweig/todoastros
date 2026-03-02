"use client"

import { useEffect, useState, Suspense } from "react"
import { useSearchParams } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useLanguage } from "@/contexts/language-context"
import { LanguageSwitcher } from "@/components/language-switcher"

// Componente interno que usa useSearchParams
function ViewChartContent() {
  const { t } = useLanguage()
  const searchParams = useSearchParams()
  const chartData = searchParams.get("data")
  const [loading, setLoading] = useState(true)
  const [chartInfo, setChartInfo] = useState<any>(null)
  const [activeTab, setActiveTab] = useState("general")

  useEffect(() => {
    if (chartData) {
      try {
        const decodedData = JSON.parse(decodeURIComponent(chartData))
        setChartInfo(decodedData)
      } catch (error) {
        console.error("Error parsing chart data:", error)
      }
    }

    // Simular tiempo de carga
    const timer = setTimeout(() => {
      setLoading(false)
    }, 1500)

    return () => clearTimeout(timer)
  }, [chartData])

  if (!chartData) {
    return (
      <Card className="p-8 max-w-md text-center">
        <h1 className="text-2xl font-bold mb-4">{t("view.error.title")}</h1>
        <p className="mb-6">{t("view.error.message")}</p>
        <Link href="/">
          <Button>{t("view.back")}</Button>
        </Link>
      </Card>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 flex flex-col flex-grow">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">{t("view.title")}</h1>
        <div className="flex gap-2">
          <Link href="/confirmation">
            <Button variant="outline">{t("view.back")}</Button>
          </Link>
        </div>
      </div>

      {loading ? (
        <div className="flex-grow flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      ) : (
        <div className="flex-grow bg-white dark:bg-slate-800 rounded-lg shadow-lg overflow-hidden">
          {chartInfo && (
            <div className="p-6">
              <CardHeader className="text-center pb-2">
                <CardTitle className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                  {t("chart.title")} {chartInfo.chartData.name}
                </CardTitle>
                <p className="text-slate-600 dark:text-slate-300">
                  {t("chart.birthdate")}: {chartInfo.chartData.birthDate}
                  {chartInfo.chartData.birthTime && ` - ${chartInfo.chartData.birthTime}`}
                  {chartInfo.chartData.birthPlace && ` - ${chartInfo.chartData.birthPlace}`}
                </p>
              </CardHeader>

              <Tabs defaultValue="general" className="w-full mt-6" onValueChange={setActiveTab}>
                <TabsList className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 mb-6">
                  <TabsTrigger value="general">{t("chart.tab.general")}</TabsTrigger>
                  <TabsTrigger value="zodiac">{t("chart.tab.zodiac")}</TabsTrigger>
                  <TabsTrigger value="planets">{t("chart.tab.planets")}</TabsTrigger>
                  {chartInfo.chartData.plan === "premium" && (
                    <>
                      <TabsTrigger value="music">{t("chart.tab.music")}</TabsTrigger>
                      <TabsTrigger value="weather">{t("chart.tab.weather")}</TabsTrigger>
                      <TabsTrigger value="news">{t("chart.tab.news")}</TabsTrigger>
                    </>
                  )}
                </TabsList>

                <TabsContent value="general" className="space-y-4">
                  <Card>
                    <CardContent className="pt-6">
                      <h3 className="text-xl font-semibold mb-4 text-indigo-600 dark:text-indigo-400">
                        {t("chart.general.title")}
                      </h3>
                      <div className="prose dark:prose-invert max-w-none">
                        {chartInfo.astrologyData?.responses?.astro_report?.report ? (
                          <div className="whitespace-pre-line">
                            {chartInfo.astrologyData.responses.astro_report.report}
                          </div>
                        ) : (
                          <p>{t("chart.general.default")}</p>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="zodiac" className="space-y-4">
                  <Card>
                    <CardContent className="pt-6">
                      <h3 className="text-xl font-semibold mb-4 text-indigo-600 dark:text-indigo-400">
                        {t("chart.zodiac.title")}
                      </h3>
                      {chartInfo.astrologyData?.responses?.zodiac ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
                            <h4 className="font-medium text-lg mb-2">{t("chart.zodiac.western")}</h4>
                            <p className="text-2xl font-bold mb-2">
                              {chartInfo.astrologyData.responses.zodiac.western_zodiac}
                            </p>
                            <p>
                              {t(
                                `chart.zodiac.${chartInfo.astrologyData.responses.zodiac.western_zodiac.toLowerCase()}`,
                              )}
                            </p>
                          </div>
                          <div className="bg-amber-50 dark:bg-amber-900/20 p-4 rounded-lg">
                            <h4 className="font-medium text-lg mb-2">{t("chart.zodiac.chinese")}</h4>
                            <p className="text-2xl font-bold mb-2">
                              {chartInfo.astrologyData.responses.zodiac.chinese_zodiac}
                            </p>
                            <p>
                              {t(
                                `chart.zodiac.${chartInfo.astrologyData.responses.zodiac.chinese_zodiac.toLowerCase()}`,
                              )}
                            </p>
                          </div>
                        </div>
                      ) : (
                        <p>{t("chart.zodiac.default")}</p>
                      )}
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="planets" className="space-y-4">
                  <Card>
                    <CardContent className="pt-6">
                      <h3 className="text-xl font-semibold mb-4 text-indigo-600 dark:text-indigo-400">
                        {t("chart.planets.title")}
                      </h3>
                      {chartInfo.astrologyData?.responses?.astronomy ? (
                        <div className="space-y-4">
                          <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
                            <h4 className="font-medium text-lg mb-2">{t("chart.planets.moon")}</h4>
                            <p>{chartInfo.astrologyData.responses.astronomy.moon_phase}</p>
                          </div>
                          <div>
                            <h4 className="font-medium text-lg mb-2">{t("chart.planets.positions")}</h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                              {chartInfo.astrologyData.responses.astronomy.planetary_positions.map(
                                (planet: any, index: number) => (
                                  <div key={index} className="bg-slate-100 dark:bg-slate-700 p-3 rounded-lg">
                                    <p className="font-semibold">{planet.planet}</p>
                                    <p className="text-sm text-slate-600 dark:text-slate-300">
                                      RA: {planet.ra}, Dec: {planet.dec}
                                    </p>
                                  </div>
                                ),
                              )}
                            </div>
                          </div>
                        </div>
                      ) : (
                        <p>{t("chart.planets.default")}</p>
                      )}
                    </CardContent>
                  </Card>
                </TabsContent>

                {chartInfo.chartData.plan === "premium" && (
                  <>
                    <TabsContent value="music" className="space-y-4">
                      <Card>
                        <CardContent className="pt-6">
                          <h3 className="text-xl font-semibold mb-4 text-indigo-600 dark:text-indigo-400">
                            {t("chart.music.title")}
                          </h3>
                          {chartInfo.astrologyData?.responses?.music?.top_songs?.length > 0 ? (
                            <div className="space-y-4">
                              <p className="mb-4">{t("chart.music.description")}</p>
                              <div className="overflow-x-auto">
                                <table className="w-full border-collapse">
                                  <thead>
                                    <tr className="bg-slate-100 dark:bg-slate-700">
                                      <th className="p-2 text-left">{t("chart.music.rank")}</th>
                                      <th className="p-2 text-left">{t("chart.music.song")}</th>
                                      <th className="p-2 text-left">{t("chart.music.artist")}</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {chartInfo.astrologyData.responses.music.top_songs.map(
                                      (song: any, index: number) => (
                                        <tr key={index} className="border-b border-slate-200 dark:border-slate-700">
                                          <td className="p-2">{song.rank}</td>
                                          <td className="p-2">{song.song}</td>
                                          <td className="p-2">{song.artist}</td>
                                        </tr>
                                      ),
                                    )}
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          ) : (
                            <p>{t("chart.music.default")}</p>
                          )}
                        </CardContent>
                      </Card>
                    </TabsContent>

                    <TabsContent value="weather" className="space-y-4">
                      <Card>
                        <CardContent className="pt-6">
                          <h3 className="text-xl font-semibold mb-4 text-indigo-600 dark:text-indigo-400">
                            {t("chart.weather.title")}
                          </h3>
                          {chartInfo.astrologyData?.responses?.weather ? (
                            <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
                              <p className="mb-2">
                                {t("chart.weather.description", {
                                  city: chartInfo.chartData.birthPlace || t("chart.weather.unknown_city"),
                                  date: chartInfo.chartData.birthDate,
                                })}
                              </p>
                              <div className="flex items-center gap-4 mt-4">
                                <div className="text-4xl font-bold">
                                  {chartInfo.astrologyData.responses.weather.temperature}°C
                                </div>
                                <div>
                                  <p className="text-lg font-medium">
                                    {chartInfo.astrologyData.responses.weather.description}
                                  </p>
                                  <p className="text-sm text-slate-600 dark:text-slate-300">
                                    {t("chart.weather.influence")}
                                  </p>
                                </div>
                              </div>
                            </div>
                          ) : (
                            <p>{t("chart.weather.default")}</p>
                          )}
                        </CardContent>
                      </Card>
                    </TabsContent>

                    <TabsContent value="news" className="space-y-4">
                      <Card>
                        <CardContent className="pt-6">
                          <h3 className="text-xl font-semibold mb-4 text-indigo-600 dark:text-indigo-400">
                            {t("chart.news.title")}
                          </h3>
                          {chartInfo.astrologyData?.responses?.news?.news_summary ? (
                            <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg">
                              <h4 className="font-medium text-lg mb-2">
                                {t("chart.news.context", {
                                  date: chartInfo.chartData.birthDate,
                                  city: chartInfo.chartData.birthPlace || t("chart.news.unknown_city"),
                                })}
                              </h4>
                              <div className="whitespace-pre-line mt-4">
                                {chartInfo.astrologyData.responses.news.news_summary}
                              </div>
                            </div>
                          ) : (
                            <p>{t("chart.news.default")}</p>
                          )}
                        </CardContent>
                      </Card>
                    </TabsContent>
                  </>
                )}
              </Tabs>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// Componente principal que envuelve el contenido en Suspense
export default function ViewChartPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col">
      <div className="absolute top-4 right-4 z-20">
        <LanguageSwitcher />
      </div>

      <Suspense
        fallback={
          <div className="flex-grow flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
        }
      >
        <ViewChartContent />
      </Suspense>
    </div>
  )
}

