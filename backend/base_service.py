from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_service(name, port):
    """Crea un servicio FastAPI con configuración común"""
    app = FastAPI(title=f"AstroFuturo {name} Service")
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En producción, limitar a dominios específicos
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {"status": "ok", "service": name}
    
    def run():
        """Ejecuta el servicio en el puerto especificado"""
        # Escuchar en todas las interfaces (0.0.0.0) en lugar de solo localhost
        uvicorn.run(app, host="0.0.0.0", port=port)
        
    return app, run

