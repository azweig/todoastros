"use client"

import { LanguageProvider } from "@/contexts/language-context"
import type { ReactNode } from "react"

export function ClientLanguageProvider({ children }: { children: ReactNode }) {
  return <LanguageProvider>{children}</LanguageProvider>
}

