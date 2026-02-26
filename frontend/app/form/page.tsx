import { AstroForm } from "@/components/astro-form"

export default function FormPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center p-4">
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="stars-bg"></div>
      </div>
      <div className="w-full max-w-2xl z-10">
        <AstroForm />
      </div>
    </div>
  )
}

