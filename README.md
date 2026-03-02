# 🌟 TodoAstros

Plataforma de astrología personalizada con generación de cartas astrales, reportes PDF, y servicios integrados de música, clima y noticias.

**Producción:** https://todoastros.com

---

## 📁 Estructura del Proyecto

```
todoastros/
├── frontend/          # Next.js 14 + Radix UI + Tailwind
├── backend/           # Python FastAPI microservicios
├── api/               # API routes adicionales
├── components/        # Componentes React compartidos
├── contexts/          # React contexts
├── hooks/             # Custom React hooks
├── lib/               # Utilidades compartidas
├── nginx/             # Configuración nginx
└── scripts/           # Scripts de deployment y mantenimiento
```

---

## 🚀 Arquitectura

### Frontend (Next.js)
- **Framework:** Next.js 14 con App Router
- **UI:** Radix UI + Tailwind CSS + shadcn/ui
- **Páginas:**
  - `/` - Landing page
  - `/form` - Formulario de datos astrológicos
  - `/pricing` - Planes y precios
  - `/payment` - Procesamiento de pagos
  - `/view-chart` - Visualización de carta astral
  - `/confirmation` - Confirmación de compra
  - `/auth` - Autenticación

### Backend (Microservicios Python)

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| `api_gateway` | 6000 | Gateway principal, enruta a servicios |
| `auth_service` | 5050 | Autenticación JWT |
| `zodiac_service` | 5001 | Datos zodiacales |
| `music_service` | 5002 | Recomendaciones musicales |
| `astronomy_service` | 5003 | Cálculos astronómicos |
| `weather_service` | 5004 | Datos meteorológicos |
| `astro_report_service` | 5006 | Generación de reportes |
| `news_service` | 5007 | Noticias astrológicas |
| `pdf_service` | 5008 | Generación de PDFs |
| `compatibility_service` | 5009 | Compatibilidad de signos |
| `location_service` | 5011 | Geolocalización |
| `email_service` | 5012 | Envío de emails |
| `whatsapp_service` | 5013 | Integración WhatsApp |
| `payment_service` | 5014 | Procesamiento de pagos |

---

## 🛠️ Instalación Local

### Requisitos
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose (recomendado)
- pnpm o npm

### Frontend

```bash
cd frontend
npm install
npm run dev
# Abre http://localhost:3000
```

### Backend (con Docker)

```bash
cd backend
docker-compose up -d
# API Gateway disponible en http://localhost:6000
```

### Backend (sin Docker)

```bash
cd backend
pip install -r requirements.txt

# Iniciar servicios individuales
cd zodiac_service && uvicorn main:app --port 5001 &
cd ../astronomy_service && uvicorn main:app --port 5003 &
# ... etc
```

---

## 🔧 Configuración

### Variables de Entorno

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:6000
NEXT_PUBLIC_STRIPE_KEY=pk_...
```

**Backend** (en `docker-compose.yml` o `.env`):
```env
JWT_SECRET_KEY=tu_secret_key
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_...
SENDGRID_API_KEY=SG...
```

---

## 📦 Deployment (Producción)

### Servidor: todoastros.com

```bash
# SSH al servidor
ssh root@todoastros.com

# Ubicación del proyecto
cd /var/www/todoastros

# Pull cambios
git pull origin main

# Rebuild frontend
cd frontend && npm run build && pm2 restart todoastros-frontend

# Rebuild backend (Docker)
cd ../backend && docker-compose up -d --build
```

### Nginx
Configuración en `/etc/nginx/sites-available/todoastros.com`

---

## 🧪 Testing

```bash
# Frontend
cd frontend && npm run lint

# Backend health check
curl http://localhost:6000/health

# Test servicios individuales
curl http://localhost:5001/zodiac/aries
```

---

## 📝 API Endpoints Principales

### Autenticación
- `POST /auth/login` - Login
- `POST /auth/register` - Registro

### Astrología
- `GET /zodiac/{sign}` - Info de signo
- `POST /astro_report/generate` - Generar reporte
- `POST /compatibility/check` - Verificar compatibilidad
- `GET /astronomy/positions` - Posiciones planetarias

### Servicios
- `POST /pdf/generate` - Generar PDF
- `POST /email/send` - Enviar email
- `POST /payment/create` - Crear pago

---

## 🔒 Seguridad

- Autenticación JWT con refresh tokens
- CORS configurado para dominio de producción
- Rate limiting en API Gateway
- Validación de inputs con Pydantic
- HTTPS forzado en producción

---

## 👥 Equipo

- **Alvaro Zweig** - Founder & Product
- **Lucky Lobster 🦞** - Development & DevOps

---

## 📄 Licencia

Propietario - TodoAstros © 2024-2026
