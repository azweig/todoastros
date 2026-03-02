"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { format } from "date-fns"
import { es, enUS } from "date-fns/locale"
import { CalendarIcon, Clock, MapPin, CreditCard, Mail } from "lucide-react"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/contexts/language-context"
import { LanguageSwitcher } from "./language-switcher"
import { generateChart } from "@/app/actions/generate-chart"

export function AstroForm() {
  const { t, language } = useLanguage()
  const [isLoading, setIsLoading] = useState(false)
  const [date, setDate] = useState<Date | undefined>(undefined)
  const [birthTime, setBirthTime] = useState("")
  const [selectedPlan, setSelectedPlan] = useState<string>("free")
  const [yearSelectOpen, setYearSelectOpen] = useState(false)
  const [monthSelectOpen, setMonthSelectOpen] = useState(false)
  const [selectedYear, setSelectedYear] = useState<number | null>(null)
  const [selectedMonth, setSelectedMonth] = useState<number | null>(null)

  // Generate years from 1900 to current year
  const currentYear = new Date().getFullYear()
  const years = Array.from({ length: currentYear - 1900 + 1 }, (_, i) => currentYear - i)

  // Generate months
  const months = Array.from({ length: 12 }, (_, i) => i)

  const monthNames = {
    es: [
      "Enero",
      "Febrero",
      "Marzo",
      "Abril",
      "Mayo",
      "Junio",
      "Julio",
      "Agosto",
      "Septiembre",
      "Octubre",
      "Noviembre",
      "Diciembre",
    ],
    en: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
  }

  useEffect(() => {
    // Get the selected plan from localStorage
    const plan = localStorage.getItem("selectedPlan")
    if (plan) {
      setSelectedPlan(plan)
    }
  }, [])

  const handleYearSelect = (year: string) => {
    setSelectedYear(Number.parseInt(year))
    setYearSelectOpen(false)

    // If month is already selected, update the date
    if (selectedMonth !== null) {
      const newDate = new Date(Number.parseInt(year), selectedMonth, 15)
      setDate(newDate)
    }
  }

  const handleMonthSelect = (month: string) => {
    const monthIndex = Number.parseInt(month)
    setSelectedMonth(monthIndex)
    setMonthSelectOpen(false)

    // If year is already selected, update the date
    if (selectedYear !== null) {
      const newDate = new Date(selectedYear, monthIndex, 15)
      setDate(newDate)
    }
  }

  const handleSubmit = async (formData: FormData) => {
    setIsLoading(true)

    // Añadir la fecha de nacimiento formateada
    if (date) {
      formData.append("birthDate", format(date, "yyyy-MM-dd"))
    }

    // Añadir el plan seleccionado
    formData.append("plan", selectedPlan)

    try {
      await generateChart(formData)
    } catch (error) {
      console.error("Error:", error)
      setIsLoading(false)
    }
  }

  return (
    <Card className="w-full shadow-lg border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm">
      <CardHeader className="space-y-1 text-center">
        <div className="absolute top-4 right-4 z-20">
          <LanguageSwitcher />
        </div>
        <CardTitle className="text-2xl font-bold">
          {selectedPlan === "premium" ? t("form.premium.title") : t("form.free.title")}
        </CardTitle>
        <CardDescription>{selectedPlan === "premium" ? t("form.premium.desc") : t("form.free.desc")}</CardDescription>
        {selectedPlan === "premium" && (
          <div className="mt-2 inline-flex items-center justify-center px-4 py-1 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 text-sm font-medium">
            <CreditCard className="h-4 w-4 mr-2" />
            {t("form.premium.badge")}
          </div>
        )}
      </CardHeader>
      <CardContent>
        <form action={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="fullName">{t("form.name")}</Label>
            <Input
              id="fullName"
              name="fullName"
              placeholder={t("form.name.placeholder")}
              required
              disabled={isLoading}
            />
          </div>

          <div className="space-y-2">
            <Label>{t("form.birthdate")}</Label>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <Select onValueChange={handleYearSelect} open={yearSelectOpen} onOpenChange={setYearSelectOpen}>
                  <SelectTrigger>
                    <SelectValue placeholder={language === "es" ? "Año" : "Year"} />
                  </SelectTrigger>
                  <SelectContent className="max-h-[200px] overflow-y-auto">
                    {years.map((year) => (
                      <SelectItem key={year} value={year.toString()}>
                        {year}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Select onValueChange={handleMonthSelect} open={monthSelectOpen} onOpenChange={setMonthSelectOpen}>
                  <SelectTrigger>
                    <SelectValue placeholder={language === "es" ? "Mes" : "Month"} />
                  </SelectTrigger>
                  <SelectContent>
                    {months.map((month) => (
                      <SelectItem key={month} value={month.toString()}>
                        {monthNames[language][month]}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {selectedYear !== null && selectedMonth !== null && (
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    className={cn("w-full justify-start text-left font-normal mt-3", !date && "text-muted-foreground")}
                    disabled={isLoading}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {date
                      ? format(date, "d MMMM yyyy", { locale: language === "es" ? es : enUS })
                      : t("form.birthdate.placeholder")}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={date}
                    onSelect={setDate}
                    initialFocus
                    month={new Date(selectedYear, selectedMonth)}
                    locale={language === "es" ? es : enUS}
                  />
                </PopoverContent>
              </Popover>
            )}
          </div>

          {selectedPlan === "premium" && (
            <>
              <div className="space-y-2">
                <Label htmlFor="birthTime">{t("form.birthtime")}</Label>
                <div className="relative">
                  <Clock className="absolute left-3 top-3 h-4 w-4 text-slate-500 dark:text-slate-400" />
                  <Input
                    id="birthTime"
                    name="birthTime"
                    type="time"
                    className="pl-10"
                    value={birthTime}
                    onChange={(e) => setBirthTime(e.target.value)}
                    required
                    disabled={isLoading}
                  />
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400">{t("form.birthtime.desc")}</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="birthplace">{t("form.birthplace")}</Label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-3 h-4 w-4 text-slate-500 dark:text-slate-400" />
                  <Input
                    id="birthplace"
                    name="birthPlace"
                    placeholder={t("form.birthplace.placeholder")}
                    className="pl-10"
                    required
                    disabled={isLoading}
                  />
                </div>
                <p className="text-xs text-slate-500 dark:text-slate-400">{t("form.birthplace.desc")}</p>
              </div>
            </>
          )}

          <Separator />

          <div className="space-y-2">
            <Label htmlFor="email">{t("form.email")}</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-500 dark:text-slate-400" />
              <Input
                id="email"
                name="email"
                type="email"
                placeholder={t("form.email.placeholder")}
                className="pl-10"
                required
                disabled={isLoading}
              />
            </div>
          </div>

          {selectedPlan === "premium" && (
            <div className="bg-indigo-50 dark:bg-indigo-900/20 p-4 rounded-lg border border-indigo-100 dark:border-indigo-800">
              <h3 className="font-medium text-indigo-800 dark:text-indigo-300 mb-2">{t("form.payment")}</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mb-4">
                (En modo desarrollo, no se procesará ningún pago real)
              </p>
              <div className="space-y-3">
                <div className="space-y-1">
                  <Label htmlFor="cardNumber">{t("form.card.number")}</Label>
                  <Input
                    id="cardNumber"
                    placeholder={t("form.card.number.placeholder")}
                    required={selectedPlan === "premium"}
                    disabled={isLoading}
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <Label htmlFor="expiry">{t("form.card.expiry")}</Label>
                    <Input
                      id="expiry"
                      placeholder={t("form.card.expiry.placeholder")}
                      required={selectedPlan === "premium"}
                      disabled={isLoading}
                    />
                  </div>
                  <div className="space-y-1">
                    <Label htmlFor="cvc">{t("form.card.cvc")}</Label>
                    <Input
                      id="cvc"
                      placeholder={t("form.card.cvc.placeholder")}
                      required={selectedPlan === "premium"}
                      disabled={isLoading}
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          <Button
            type="submit"
            className={`w-full ${selectedPlan === "premium" ? "bg-indigo-600 hover:bg-indigo-700" : "bg-slate-700 hover:bg-slate-800"}`}
            disabled={isLoading || !date || (selectedPlan === "premium" && !birthTime)}
          >
            {isLoading
              ? t("form.submit.loading")
              : selectedPlan === "premium"
                ? t("form.submit.premium")
                : t("form.submit.free")}
          </Button>
        </form>
      </CardContent>
      <CardFooter className="flex justify-center">
        <p className="text-xs text-center text-slate-500 dark:text-slate-400">{t("form.data.safe")}</p>
      </CardFooter>
    </Card>
  )
}

