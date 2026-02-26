"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

type Language = "es" | "en"

type LanguageContextType = {
  language: Language
  setLanguage: (language: Language) => void
  t: (key: string) => string
}

const translations = {
  es: {
    // Landing Page
    "app.title": "AstroFuturo",
    "app.subtitle": "Descubre tu destino en las estrellas",
    "app.cta": "Crear mi carta astral",
    "app.description":
      "Sumérgete en la sabiduría ancestral de la astrología y descubre cómo los astros influyen en tu personalidad, relaciones y camino de vida. Nuestras cartas astrales combinan conocimiento milenario con tecnología moderna.",
    "feature.personalized": "Astrología Personalizada",
    "feature.personalized.desc":
      "Análisis detallado de tu carta natal basado en la posición exacta de los astros en tu nacimiento.",
    "feature.cosmic": "Conexión Cósmica",
    "feature.cosmic.desc": "Descubre cómo los eventos astronómicos y la energía universal han moldeado tu esencia.",
    "feature.spiritual": "Guía Espiritual",
    "feature.spiritual.desc":
      "Recibe consejos prácticos para aprovechar tus fortalezas y superar los desafíos en tu camino.",

    // Pricing Page
    "pricing.title": "Elige tu viaje astral",
    "pricing.subtitle":
      "Descubre las estrellas a tu manera. Elige entre nuestra carta astral básica gratuita o la experiencia premium con detalles personalizados.",
    "pricing.free.title": "Carta Astral Básica",
    "pricing.free.price": "Gratis",
    "pricing.free.desc": "Descubre los fundamentos de tu carta astral",
    "pricing.premium.title": "Carta Astral Premium",
    "pricing.premium.price": "$5 USD",
    "pricing.premium.desc": "Análisis profundo y personalizado",
    "pricing.recommended": "Recomendado",
    "pricing.free.select": "Seleccionar Plan Gratuito",
    "pricing.premium.select": "Obtener Plan Premium",
    "pricing.back": "Volver al inicio",

    // Features
    "feature.basic.analysis": "Análisis básico de tu signo zodiacal",
    "feature.compatibility": "Compatibilidad con otros signos",
    "feature.general.predictions": "Predicciones generales",
    "feature.no.exact.time": "Sin análisis de hora exacta",
    "feature.no.music": "Sin recomendaciones musicales",
    "feature.no.historical": "Sin análisis de eventos históricos",
    "feature.no.weather": "Sin análisis climático",
    "feature.detailed.analysis": "Análisis detallado de tu carta natal completa",
    "feature.houses": "Interpretación de casas astrológicas",
    "feature.planetary": "Análisis de aspectos planetarios",
    "feature.exact.time": "Análisis preciso con hora exacta de nacimiento",
    "feature.music": "Top 10 canciones populares de tu fecha de nacimiento",
    "feature.historical": "Eventos históricos de tu día de nacimiento",
    "feature.weather": "Análisis del clima en tu ciudad natal",

    // Form
    "form.free.title": "Carta Astral Básica",
    "form.premium.title": "Carta Astral Premium",
    "form.free.desc": "Completa la información para generar tu carta astral básica gratuita",
    "form.premium.desc": "Completa la información para generar tu carta astral personalizada premium",
    "form.premium.badge": "Plan Premium - $5 USD",
    "form.name": "Nombre completo",
    "form.name.placeholder": "Ingresa tu nombre completo",
    "form.birthdate": "Fecha de nacimiento",
    "form.birthdate.placeholder": "Selecciona una fecha",
    "form.birthtime": "Hora de nacimiento",
    "form.birthtime.desc": "La hora exacta nos permite un análisis más preciso de tu carta astral",
    "form.birthplace": "Ciudad de nacimiento",
    "form.birthplace.placeholder": "Ingresa tu ciudad de nacimiento",
    "form.birthplace.desc": "Ingresa el nombre de tu ciudad para autocompletar",
    "form.email": "Correo electrónico",
    "form.email.placeholder": "tu@email.com",
    "form.payment": "Información de pago",
    "form.card.number": "Número de tarjeta",
    "form.card.number.placeholder": "1234 5678 9012 3456",
    "form.card.expiry": "Fecha de expiración",
    "form.card.expiry.placeholder": "MM/AA",
    "form.card.cvc": "CVC",
    "form.card.cvc.placeholder": "123",
    "form.submit.loading": "Generando...",
    "form.submit.free": "Generar Mi Carta Astral Gratuita",
    "form.submit.premium": "Pagar $5 y Generar Mi Carta Astral",
    "form.data.safe": "Tus datos están seguros y solo se utilizarán para generar tu carta astral",

    // Confirmation
    "confirm.free.title": "¡Tu carta astral básica está en camino!",
    "confirm.premium.title": "¡Tu carta astral premium está en camino!",
    "confirm.free.desc": "Estamos consultando las estrellas para crear tu informe básico",
    "confirm.premium.desc": "Estamos consultando las estrellas para crear tu informe personalizado premium",
    "confirm.progress": "Progreso",
    "confirm.free.success":
      "Tu carta astral básica ha sido generada con éxito y será enviada en breve a tu correo electrónico.",
    "confirm.premium.success":
      "Tu carta astral premium ha sido generada con éxito y será enviada en breve a tu correo electrónico.",
    "confirm.free.processing":
      "Estamos analizando tu fecha de nacimiento para crear un informe básico con información general sobre tu signo.",
    "confirm.premium.processing":
      "Estamos analizando tu fecha, hora y lugar de nacimiento para crear un informe detallado y personalizado con todos los beneficios premium.",
    "confirm.premium.benefits": "Beneficios Premium",
    "confirm.back": "Volver al inicio",
    "confirm.view.chart": "Ver mi carta astral",

    // Language
    "language.switch": "Switch to English",

    // View
    "view.title": "Tu Carta Astral",
    "view.back": "Volver",
    "view.download": "Descargar PDF",
    "view.error.title": "Error al cargar la carta astral",
    "view.error.message": "No se pudo encontrar la URL de la carta astral. Por favor, vuelve a intentarlo.",

    // Error
    "error.title": "Ha ocurrido un error",
    "error.default": "Lo sentimos, ha ocurrido un error inesperado.",
    "error.back": "Volver al inicio",

    // Chart
    "chart.title": "Carta Astral para",
    "chart.birthdate": "Fecha de nacimiento",
    "chart.tab.general": "General",
    "chart.tab.zodiac": "Signos",
    "chart.tab.planets": "Planetas",
    "chart.tab.music": "Música",
    "chart.tab.weather": "Clima",
    "chart.tab.news": "Contexto",

    "chart.general.title": "Análisis Astrológico",
    "chart.general.default":
      "Tu carta astral revela aspectos fascinantes de tu personalidad y destino. Los astros en el momento de tu nacimiento han influido en tu carácter y en las energías que te acompañan a lo largo de tu vida.",

    "chart.zodiac.title": "Tus Signos Zodiacales",
    "chart.zodiac.western": "Signo Occidental",
    "chart.zodiac.chinese": "Signo Chino",
    "chart.zodiac.default": "No se pudo determinar tu signo zodiacal con la información proporcionada.",
    "chart.zodiac.aries":
      "Aries es el primer signo del zodíaco, caracterizado por su energía, iniciativa y valentía. Las personas nacidas bajo este signo suelen ser dinámicas, directas y apasionadas.",
    "chart.zodiac.tauro":
      "Tauro es el segundo signo del zodíaco, conocido por su determinación, sensualidad y practicidad. Las personas nacidas bajo este signo suelen ser estables, leales y aprecian los placeres de la vida.",
    "chart.zodiac.géminis":
      "Géminis es el tercer signo del zodíaco, destacado por su curiosidad, adaptabilidad y comunicación. Las personas nacidas bajo este signo suelen ser versátiles, intelectuales y sociables.",
    "chart.zodiac.cáncer":
      "Cáncer es el cuarto signo del zodíaco, caracterizado por su intuición, sensibilidad y protección. Las personas nacidas bajo este signo suelen ser emotivas, cuidadoras y con fuerte conexión familiar.",
    "chart.zodiac.leo":
      "Leo es el quinto signo del zodíaco, conocido por su creatividad, generosidad y liderazgo. Las personas nacidas bajo este signo suelen ser carismáticas, orgullosas y con gran vitalidad.",
    "chart.zodiac.virgo":
      "Virgo es el sexto signo del zodíaco, destacado por su análisis, perfeccionismo y servicio. Las personas nacidas bajo este signo suelen ser metódicas, prácticas y atentas a los detalles.",
    "chart.zodiac.libra":
      "Libra es el séptimo signo del zodíaco, caracterizado por su equilibrio, diplomacia y apreciación por la belleza. Las personas nacidas bajo este signo suelen ser justas, sociables y buscan la armonía.",
    "chart.zodiac.escorpio":
      "Escorpio es el octavo signo del zodíaco, conocido por su intensidad, pasión y transformación. Las personas nacidas bajo este signo suelen ser profundas, determinadas y con gran fuerza interior.",
    "chart.zodiac.sagitario":
      "Sagitario es el noveno signo del zodíaco, destacado por su optimismo, libertad y búsqueda de la verdad. Las personas nacidas bajo este signo suelen ser aventureras, filosóficas y directas.",
    "chart.zodiac.capricornio":
      "Capricornio es el décimo signo del zodíaco, caracterizado por su ambición, disciplina y responsabilidad. Las personas nacidas bajo este signo suelen ser trabajadoras, perseverantes y con gran sentido práctico.",
    "chart.zodiac.acuario":
      "Acuario es el undécimo signo del zodíaco, conocido por su originalidad, independencia y visión de futuro. Las personas nacidas bajo este signo suelen ser innovadoras, humanitarias y con pensamiento progresista.",
    "chart.zodiac.piscis":
      "Piscis es el duodécimo signo del zodíaco, destacado por su compasión, intuición y conexión espiritual. Las personas nacidas bajo este signo suelen ser sensibles, imaginativas y con gran empatía.",

    "chart.zodiac.rata":
      "La Rata en el zodíaco chino simboliza el ingenio, la adaptabilidad y la vitalidad. Las personas nacidas en el año de la Rata suelen ser inteligentes, versátiles y con gran capacidad de supervivencia.",
    "chart.zodiac.buey":
      "El Buey en el zodíaco chino simboliza la diligencia, la confiabilidad y la determinación. Las personas nacidas en el año del Buey suelen ser trabajadoras, pacientes y con gran fuerza de voluntad.",
    "chart.zodiac.tigre":
      "El Tigre en el zodíaco chino simboliza la valentía, la competitividad y el carisma. Las personas nacidas en el año del Tigre suelen ser valientes, apasionadas y con gran energía.",
    "chart.zodiac.conejo":
      "El Conejo en el zodíaco chino simboliza la compasión, la elegancia y la prudencia. Las personas nacidas en el año del Conejo suelen ser amables, refinadas y con gran sensibilidad.",
    "chart.zodiac.dragón":
      "El Dragón en el zodíaco chino simboliza el entusiasmo, la confianza y la ambición. Las personas nacidas en el año del Dragón suelen ser carismáticas, enérgicas y con gran fuerza vital.",
    "chart.zodiac.serpiente":
      "La Serpiente en el zodíaco chino simboliza la intuición, la sabiduría y la elegancia. Las personas nacidas en el año de la Serpiente suelen ser reflexivas, misteriosas y con gran profundidad.",
    "chart.zodiac.caballo":
      "El Caballo en el zodíaco chino simboliza la energía, la independencia y la sociabilidad. Las personas nacidas en el año del Caballo suelen ser dinámicas, aventureras y con gran espíritu libre.",
    "chart.zodiac.cabra":
      "La Cabra en el zodíaco chino simboliza la creatividad, la empatía y la sensibilidad. Las personas nacidas en el año de la Cabra suelen ser artísticas, compasivas y con gran intuición.",
    "chart.zodiac.mono":
      "El Mono en el zodíaco chino simboliza la inteligencia, la curiosidad y la versatilidad. Las personas nacidas en el año del Mono suelen ser ingeniosas, adaptables y con gran sentido del humor.",
    "chart.zodiac.gallo":
      "El Gallo en el zodíaco chino simboliza la observación, la honestidad y la meticulosidad. Las personas nacidas en el año del Gallo suelen ser detallistas, trabajadoras y con gran sentido de la responsabilidad.",
    "chart.zodiac.perro":
      "El Perro en el zodíaco chino simboliza la lealtad, la justicia y el altruismo. Las personas nacidas en el año del Perro suelen ser fieles, honestas y con gran sentido del deber.",
    "chart.zodiac.cerdo":
      "El Cerdo en el zodíaco chino simboliza la generosidad, la sinceridad y el disfrute de la vida. Las personas nacidas en el año del Cerdo suelen ser amables, optimistas y con gran capacidad para disfrutar los placeres.",

    "chart.planets.title": "Posiciones Planetarias",
    "chart.planets.moon": "Fase Lunar",
    "chart.planets.positions": "Posiciones de los Planetas",
    "chart.planets.default": "No se pudieron determinar las posiciones planetarias con la información proporcionada.",

    "chart.music.title": "Música Popular en tu Nacimiento",
    "chart.music.description":
      "Estas eran las canciones más populares cerca de tu fecha de nacimiento. La música que sonaba cuando llegaste al mundo puede tener una conexión especial contigo.",
    "chart.music.rank": "Posición",
    "chart.music.song": "Canción",
    "chart.music.artist": "Artista",
    "chart.music.default": "No se pudo obtener información sobre la música popular en tu fecha de nacimiento.",

    "chart.weather.title": "Clima en tu Nacimiento",
    "chart.weather.description": "El clima en {city} el día {date} era:",
    "chart.weather.unknown_city": "tu ciudad natal",
    "chart.weather.influence":
      "Según algunas tradiciones astrológicas, el clima en el momento del nacimiento puede influir en ciertos aspectos del temperamento.",
    "chart.weather.default": "No se pudo obtener información sobre el clima en tu fecha y lugar de nacimiento.",

    "chart.news.title": "Contexto Histórico y Cultural",
    "chart.news.context": "El {date} en {city}:",
    "chart.news.unknown_city": "tu lugar de nacimiento",
    "chart.news.default":
      "No se pudo obtener información sobre el contexto histórico y cultural de tu fecha y lugar de nacimiento.",
  },
  en: {
    // Landing Page
    "app.title": "AstroFuture",
    "app.subtitle": "Discover your destiny in the stars",
    "app.cta": "Create my astral chart",
    "app.description":
      "Immerse yourself in the ancient wisdom of astrology and discover how the stars influence your personality, relationships, and life path. Our astral charts combine ancient knowledge with modern technology.",
    "feature.personalized": "Personalized Astrology",
    "feature.personalized.desc":
      "Detailed analysis of your natal chart based on the exact position of the stars at your birth.",
    "feature.cosmic": "Cosmic Connection",
    "feature.cosmic.desc": "Discover how astronomical events and universal energy have shaped your essence.",
    "feature.spiritual": "Spiritual Guidance",
    "feature.spiritual.desc":
      "Receive practical advice to leverage your strengths and overcome challenges in your path.",

    // Pricing Page
    "pricing.title": "Choose your astral journey",
    "pricing.subtitle":
      "Discover the stars your way. Choose between our free basic astral chart or the premium experience with personalized details.",
    "pricing.free.title": "Basic Astral Chart",
    "pricing.free.price": "Free",
    "pricing.free.desc": "Discover the fundamentals of your astral chart",
    "pricing.premium.title": "Premium Astral Chart",
    "pricing.premium.price": "$5 USD",
    "pricing.premium.desc": "Deep and personalized analysis",
    "pricing.recommended": "Recommended",
    "pricing.free.select": "Select Free Plan",
    "pricing.premium.select": "Get Premium Plan",
    "pricing.back": "Back to home",

    // Features
    "feature.basic.analysis": "Basic analysis of your zodiac sign",
    "feature.compatibility": "Compatibility with other signs",
    "feature.general.predictions": "General predictions",
    "feature.no.exact.time": "No exact time analysis",
    "feature.no.music": "No music recommendations",
    "feature.no.historical": "No historical events analysis",
    "feature.no.weather": "No weather analysis",
    "feature.detailed.analysis": "Detailed analysis of your complete natal chart",
    "feature.houses": "Interpretation of astrological houses",
    "feature.planetary": "Analysis of planetary aspects",
    "feature.exact.time": "Precise analysis with exact birth time",
    "feature.music": "Top 10 popular songs from your birth date",
    "feature.historical": "Historical events from your birth day",
    "feature.weather": "Weather analysis in your birth city",

    // Form
    "form.free.title": "Basic Astral Chart",
    "form.premium.title": "Premium Astral Chart",
    "form.free.desc": "Complete the information to generate your free basic astral chart",
    "form.premium.desc": "Complete the information to generate your personalized premium astral chart",
    "form.premium.badge": "Premium Plan - $5 USD",
    "form.name": "Full name",
    "form.name.placeholder": "Enter your full name",
    "form.birthdate": "Date of birth",
    "form.birthdate.placeholder": "Select a date",
    "form.birthtime": "Time of birth",
    "form.birthtime.desc": "The exact time allows us to create a more precise astral chart",
    "form.birthplace": "City of birth",
    "form.birthplace.placeholder": "Enter your birth city",
    "form.birthplace.desc": "Enter your city name for autocomplete",
    "form.email": "Email address",
    "form.email.placeholder": "you@email.com",
    "form.payment": "Payment information",
    "form.card.number": "Card number",
    "form.card.number.placeholder": "1234 5678 9012 3456",
    "form.card.expiry": "Expiration date",
    "form.card.expiry.placeholder": "MM/YY",
    "form.card.cvc": "CVC",
    "form.card.cvc.placeholder": "123",
    "form.submit.loading": "Generating...",
    "form.submit.free": "Generate My Free Astral Chart",
    "form.submit.premium": "Pay $5 and Generate My Astral Chart",
    "form.data.safe": "Your data is secure and will only be used to generate your astral chart",

    // Confirmation
    "confirm.free.title": "Your basic astral chart is on its way!",
    "confirm.premium.title": "Your premium astral chart is on its way!",
    "confirm.free.desc": "We're consulting the stars to create your basic report",
    "confirm.premium.desc": "We're consulting the stars to create your personalized premium report",
    "confirm.progress": "Progress",
    "confirm.free.success":
      "Your basic astral chart has been successfully generated and will be sent shortly to your email.",
    "confirm.premium.success":
      "Your premium astral chart has been successfully generated and will be sent shortly to your email.",
    "confirm.free.processing":
      "We're analyzing your birth date to create a basic report with general information about your sign.",
    "confirm.premium.processing":
      "We're analyzing your date, time, and place of birth to create a detailed and personalized report with all premium benefits.",
    "confirm.premium.benefits": "Premium Benefits",
    "confirm.back": "Back to home",
    "confirm.view.chart": "View my astral chart",

    // Language
    "language.switch": "Cambiar a Español",

    // View
    "view.title": "Your Astral Chart",
    "view.back": "Back",
    "view.download": "Download PDF",
    "view.error.title": "Error loading astral chart",
    "view.error.message": "Could not find the astral chart URL. Please try again.",

    // Error
    "error.title": "An error has occurred",
    "error.default": "Sorry, an unexpected error has occurred.",
    "error.back": "Back to home",

    // Chart
    "chart.title": "Astral Chart for",
    "chart.birthdate": "Date of birth",
    "chart.tab.general": "General",
    "chart.tab.zodiac": "Signs",
    "chart.tab.planets": "Planets",
    "chart.tab.music": "Music",
    "chart.tab.weather": "Weather",
    "chart.tab.news": "Context",

    "chart.general.title": "Astrological Analysis",
    "chart.general.default":
      "Your astral chart reveals fascinating aspects of your personality and destiny. The stars at the moment of your birth have influenced your character and the energies that accompany you throughout your life.",

    "chart.zodiac.title": "Your Zodiac Signs",
    "chart.zodiac.western": "Western Sign",
    "chart.zodiac.chinese": "Chinese Sign",
    "chart.zodiac.default": "Your zodiac sign could not be determined with the information provided.",
    "chart.zodiac.aries":
      "Aries is the first sign of the zodiac, characterized by its energy, initiative, and courage. People born under this sign tend to be dynamic, direct, and passionate.",
    "chart.zodiac.tauro":
      "Taurus is the second sign of the zodiac, known for its determination, sensuality, and practicality. People born under this sign tend to be stable, loyal, and appreciate life's pleasures.",
    "chart.zodiac.géminis":
      "Gemini is the third sign of the zodiac, highlighted for its curiosity, adaptability, and communication. People born under this sign tend to be versatile, intellectual, and sociable.",
    "chart.zodiac.cáncer":
      "Cancer is the fourth sign of the zodiac, characterized by its intuition, sensitivity, and protection. People born under this sign tend to be emotional, nurturing, and have a strong family connection.",
    "chart.zodiac.leo":
      "Leo is the fifth sign of the zodiac, known for its creativity, generosity, and leadership. People born under this sign tend to be charismatic, proud, and have great vitality.",
    "chart.zodiac.virgo":
      "Virgo is the sixth sign of the zodiac, highlighted for its analysis, perfectionism, and service. People born under this sign tend to be methodical, practical, and attentive to details.",
    "chart.zodiac.libra":
      "Libra is the seventh sign of the zodiac, characterized by its balance, diplomacy, and appreciation for beauty. People born under this sign tend to be fair, sociable, and seek harmony.",
    "chart.zodiac.escorpio":
      "Scorpio is the eighth sign of the zodiac, known for its intensity, passion, and transformation. People born under this sign tend to be deep, determined, and have great inner strength.",
    "chart.zodiac.sagitario":
      "Sagittarius is the ninth sign of the zodiac, highlighted for its optimism, freedom, and search for truth. People born under this sign tend to be adventurous, philosophical, and direct.",
    "chart.zodiac.capricornio":
      "Capricorn is the tenth sign of the zodiac, characterized by its ambition, discipline, and responsibility. People born under this sign tend to be hardworking, persevering, and have great practical sense.",
    "chart.zodiac.acuario":
      "Aquarius is the eleventh sign of the zodiac, known for its originality, independence, and vision of the future. People born under this sign tend to be innovative, humanitarian, and have progressive thinking.",
    "chart.zodiac.piscis":
      "Pisces is the twelfth sign of the zodiac, highlighted for its compassion, intuition, and spiritual connection. People born under this sign tend to be sensitive, imaginative, and have great empathy.",

    "chart.zodiac.rata":
      "The Rat in Chinese zodiac symbolizes wit, adaptability, and vitality. People born in the Year of the Rat tend to be intelligent, versatile, and have great survival skills.",
    "chart.zodiac.buey":
      "The Ox in Chinese zodiac symbolizes diligence, reliability, and determination. People born in the Year of the Ox tend to be hardworking, patient, and have great willpower.",
    "chart.zodiac.tigre":
      "The Tiger in Chinese zodiac symbolizes courage, competitiveness, and charisma. People born in the Year of the Tiger tend to be brave, passionate, and have great energy.",
    "chart.zodiac.conejo":
      "The Rabbit in Chinese zodiac symbolizes compassion, elegance, and prudence. People born in the Year of the Rabbit tend to be kind, refined, and have great sensitivity.",
    "chart.zodiac.dragón":
      "The Dragon in Chinese zodiac symbolizes enthusiasm, confidence, and ambition. People born in the Year of the Dragon tend to be charismatic, energetic, and have great vitality.",
    "chart.zodiac.serpiente":
      "The Snake in Chinese zodiac symbolizes intuition, wisdom, and elegance. People born in the Year of the Snake tend to be reflective, mysterious, and have great depth.",
    "chart.zodiac.caballo":
      "The Horse in Chinese zodiac symbolizes energy, independence, and sociability. People born in the Year of the Horse tend to be dynamic, adventurous, and have a free spirit.",
    "chart.zodiac.cabra":
      "The Goat in Chinese zodiac symbolizes creativity, empathy, and sensitivity. People born in the Year of the Goat tend to be artistic, compassionate, and have great intuition.",
    "chart.zodiac.mono":
      "The Monkey in Chinese zodiac symbolizes intelligence, curiosity, and versatility. People born in the Year of the Monkey tend to be ingenious, adaptable, and have a great sense of humor.",
    "chart.zodiac.gallo":
      "The Rooster in Chinese zodiac symbolizes observation, honesty, and meticulousness. People born in the Year of the Rooster tend to be detail-oriented, hardworking, and have a great sense of responsibility.",
    "chart.zodiac.perro":
      "The Dog in Chinese zodiac symbolizes loyalty, justice, and altruism. People born in the Year of the Dog tend to be faithful, honest, and have a great sense of duty.",
    "chart.zodiac.cerdo":
      "The Pig in Chinese zodiac symbolizes generosity, sincerity, and enjoyment of life. People born in the Year of the Pig tend to be kind, optimistic, and have a great capacity to enjoy pleasures.",

    "chart.planets.title": "Planetary Positions",
    "chart.planets.moon": "Moon Phase",
    "chart.planets.positions": "Planet Positions",
    "chart.planets.default": "Planetary positions could not be determined with the information provided.",

    "chart.music.title": "Popular Music at Your Birth",
    "chart.music.description":
      "These were the most popular songs around your birth date. The music that was playing when you came into the world may have a special connection with you.",
    "chart.music.rank": "Position",
    "chart.music.song": "Song",
    "chart.music.artist": "Artist",
    "chart.music.default": "Information about popular music on your birth date could not be obtained.",

    "chart.weather.title": "Weather at Your Birth",
    "chart.weather.description": "The weather in {city} on {date} was:",
    "chart.weather.unknown_city": "your hometown",
    "chart.weather.influence":
      "According to some astrological traditions, the weather at the time of birth can influence certain aspects of temperament.",
    "chart.weather.default": "Information about the weather on your birth date and place could not be obtained.",

    "chart.news.title": "Historical and Cultural Context",
    "chart.news.context": "On {date} in {city}:",
    "chart.news.unknown_city": "your place of birth",
    "chart.news.default":
      "Information about the historical and cultural context of your birth date and place could not be obtained.",
  },
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>("es")

  useEffect(() => {
    // Solo acceder a localStorage en el cliente
    if (typeof window !== "undefined") {
      const savedLanguage = localStorage.getItem("language") as Language
      if (savedLanguage && (savedLanguage === "es" || savedLanguage === "en")) {
        setLanguageState(savedLanguage)
      }
    }
  }, [])

  const setLanguage = (newLanguage: Language) => {
    setLanguageState(newLanguage)
    // Solo acceder a localStorage en el cliente
    if (typeof window !== "undefined") {
      localStorage.setItem("language", newLanguage)
    }
  }

  const t = (key: string): string => {
    return translations[language][key as keyof (typeof translations)[typeof language]] || key
  }

  return <LanguageContext.Provider value={{ language, setLanguage, t }}>{children}</LanguageContext.Provider>
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error("useLanguage must be used within a LanguageProvider")
  }
  return context
}

