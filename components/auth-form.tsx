"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { MoonIcon, SunIcon, Mail, Lock, User } from "lucide-react"

export function AuthForm() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const handleSocialLogin = (provider: string) => {
    setIsLoading(true)
    // In a real app, this would connect to your authentication provider
    console.log(`Logging in with ${provider}`)

    // Simulate authentication delay
    setTimeout(() => {
      setIsLoading(false)
      router.push("/form")
    }, 1500)
  }

  const handleEmailLogin = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // Simulate authentication delay
    setTimeout(() => {
      setIsLoading(false)
      router.push("/form")
    }, 1500)
  }

  const handleEmailRegister = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // Simulate authentication delay
    setTimeout(() => {
      setIsLoading(false)
      router.push("/form")
    }, 1500)
  }

  return (
    <Card className="w-full shadow-lg border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm">
      <CardHeader className="space-y-1 text-center">
        <div className="flex justify-center mb-2">
          <div className="relative">
            <MoonIcon className="h-10 w-10 text-indigo-600 dark:text-indigo-400" />
            <SunIcon className="h-5 w-5 text-yellow-500 absolute -top-1 -right-1" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">Bienvenido a AstroFuturo</CardTitle>
        <CardDescription>Inicia sesión o regístrate para continuar</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Button
            variant="outline"
            className="w-full border-slate-300 dark:border-slate-600"
            onClick={() => handleSocialLogin("Google")}
            disabled={isLoading}
          >
            <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
              <path d="M1 1h22v22H1z" fill="none" />
            </svg>
            Continuar con Google
          </Button>
          <Button
            variant="outline"
            className="w-full border-slate-300 dark:border-slate-600"
            onClick={() => handleSocialLogin("Facebook")}
            disabled={isLoading}
          >
            <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
              <path
                d="M9.19795 21.5H13.198V13.4901H16.8021L17.198 9.50977H13.198V7.5C13.198 6.94772 13.6457 6.5 14.198 6.5H17.198V2.5H14.198C11.4365 2.5 9.19795 4.73858 9.19795 7.5V9.50977H7.19795L6.80206 13.4901H9.19795V21.5Z"
                fill="#1877F2"
              />
            </svg>
            Continuar con Facebook
          </Button>
        </div>
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-slate-300 dark:border-slate-600" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-white dark:bg-slate-800 px-2 text-slate-500 dark:text-slate-400">O continúa con</span>
          </div>
        </div>
        <Tabs defaultValue="login" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login">Iniciar Sesión</TabsTrigger>
            <TabsTrigger value="register">Registrarse</TabsTrigger>
          </TabsList>
          <TabsContent value="login">
            <form onSubmit={handleEmailLogin}>
              <div className="space-y-3">
                <div className="space-y-1">
                  <Label htmlFor="email">Correo electrónico</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-500 dark:text-slate-400" />
                    <Input
                      id="email"
                      placeholder="tu@email.com"
                      type="email"
                      className="pl-10"
                      required
                      disabled={isLoading}
                    />
                  </div>
                </div>
                <div className="space-y-1">
                  <Label htmlFor="password">Contraseña</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-500 dark:text-slate-400" />
                    <Input
                      id="password"
                      placeholder="••••••••"
                      type="password"
                      className="pl-10"
                      required
                      disabled={isLoading}
                    />
                  </div>
                </div>
                <Button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-700" disabled={isLoading}>
                  {isLoading ? "Iniciando sesión..." : "Iniciar Sesión"}
                </Button>
              </div>
            </form>
          </TabsContent>
          <TabsContent value="register">
            <form onSubmit={handleEmailRegister}>
              <div className="space-y-3">
                <div className="space-y-1">
                  <Label htmlFor="name">Nombre completo</Label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 h-4 w-4 text-slate-500 dark:text-slate-400" />
                    <Input
                      id="name"
                      placeholder="Tu nombre"
                      type="text"
                      className="pl-10"
                      required
                      disabled={isLoading}
                    />
                  </div>
                </div>
                <div className="space-y-1">
                  <Label htmlFor="register-email">Correo electrónico</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-500 dark:text-slate-400" />
                    <Input
                      id="register-email"
                      placeholder="tu@email.com"
                      type="email"
                      className="pl-10"
                      required
                      disabled={isLoading}
                    />
                  </div>
                </div>
                <div className="space-y-1">
                  <Label htmlFor="register-password">Contraseña</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-500 dark:text-slate-400" />
                    <Input
                      id="register-password"
                      placeholder="••••••••"
                      type="password"
                      className="pl-10"
                      required
                      disabled={isLoading}
                    />
                  </div>
                </div>
                <Button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-700" disabled={isLoading}>
                  {isLoading ? "Registrando..." : "Registrarse"}
                </Button>
              </div>
            </form>
          </TabsContent>
        </Tabs>
      </CardContent>
      <CardFooter className="flex flex-col space-y-2">
        <div className="text-xs text-center text-slate-500 dark:text-slate-400">
          Al continuar, aceptas nuestros{" "}
          <Link href="#" className="underline">
            Términos de servicio
          </Link>{" "}
          y{" "}
          <Link href="#" className="underline">
            Política de privacidad
          </Link>
        </div>
      </CardFooter>
    </Card>
  )
}

