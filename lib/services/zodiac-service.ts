// Servicio de zodíaco integrado en Next.js

interface ZodiacResponse {
  western_zodiac: string
  chinese_zodiac: string
}

export function getZodiacSign(dateOfBirth: string): ZodiacResponse {
  // Determinar el signo zodiacal occidental
  const [year, month, day] = dateOfBirth.split("-").map(Number)
  let westernZodiac = "Desconocido"

  if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) westernZodiac = "Aries"
  else if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) westernZodiac = "Tauro"
  else if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) westernZodiac = "Géminis"
  else if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) westernZodiac = "Cáncer"
  else if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) westernZodiac = "Leo"
  else if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) westernZodiac = "Virgo"
  else if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) westernZodiac = "Libra"
  else if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) westernZodiac = "Escorpio"
  else if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) westernZodiac = "Sagitario"
  else if ((month === 12 && day >= 22) || (month === 1 && day <= 19)) westernZodiac = "Capricornio"
  else if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) westernZodiac = "Acuario"
  else if ((month === 2 && day >= 19) || (month === 3 && day <= 20)) westernZodiac = "Piscis"

  // Determinar el signo zodiacal chino
  const animals = [
    "Rata",
    "Buey",
    "Tigre",
    "Conejo",
    "Dragón",
    "Serpiente",
    "Caballo",
    "Cabra",
    "Mono",
    "Gallo",
    "Perro",
    "Cerdo",
  ]
  const chineseZodiac = animals[(year - 4) % 12]

  return {
    western_zodiac: westernZodiac,
    chinese_zodiac: chineseZodiac,
  }
}

