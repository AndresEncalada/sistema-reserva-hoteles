from fastapi import FastAPI
from controllers.auth_controller import router as auth_router
from controllers.habitacion_controller import router as habitacion_router
from controllers.reserva_controller import router as reserva_router
from controllers.dashboard_controller import router as dashboard_router
from controllers.factura_controller import router as factura_router
from controllers.usuario_controller import router as usuario_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

description = """
API backend para gestionar reservas de hotel.

Funcionalidades principales:

- Autenticacion con JWT.
- Control de acceso por roles: `admin` y `user`.
- Gestion de usuarios, habitaciones, reservas y facturas.
- Dashboard administrativo con estadisticas generales.

Uso en Swagger:

1. Ejecutar `POST /api/auth/login` con las credenciales de prueba.
2. Copiar el `access_token` retornado.
3. Pulsar `Authorize` y pegar el token con formato Bearer.
"""

tags_metadata = [
    {
        "name": "Autenticación",
        "description": "Registro e inicio de sesion. Devuelve tokens JWT para consumir endpoints protegidos.",
    },
    {
        "name": "Usuarios",
        "description": "Consulta de perfil, cambio de password y administracion de usuarios.",
    },
    {
        "name": "Habitaciones",
        "description": "Busqueda, consulta y administracion de habitaciones del hotel.",
    },
    {
        "name": "Reservas",
        "description": "Creacion, consulta, pago, notificacion y cancelacion de reservas.",
    },
    {
        "name": "Facturas",
        "description": "Consulta de facturas generadas a partir de reservas pagadas.",
    },
    {
        "name": "Dashboard",
        "description": "Indicadores administrativos de reservas, habitaciones e ingresos.",
    },
]

app = FastAPI(
    title="API de Reservas de Hotel",
    description=description,
    version="1.0.0",
    contact={
        "name": "Equipo Sistema de Reserva de Hoteles",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(auth_router)
app.include_router(habitacion_router)
app.include_router(reserva_router)
app.include_router(dashboard_router)
app.include_router(factura_router)
app.include_router(usuario_router)

# Configuración para servir el frontend en producción
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"

# Solo montar si existe el directorio (producción)
if FRONTEND_DIR.exists():
    # Montar archivos estáticos (CSS, JS, imágenes)
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")
    
    # Ruta catch-all para servir index.html (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = FRONTEND_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del Hotel. Visita /docs para ver la documentación."}
