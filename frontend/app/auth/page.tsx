import { AuthForm } from "@/components/auth-form"

export default function AuthPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center p-4">
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="stars-bg"></div>
      </div>
      <div className="w-full max-w-md z-10">
        <AuthForm />
      </div>
    </div>
  )
}

