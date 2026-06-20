from fastapi import FastAPI
from controllers.auth_controller import router as auth_router
from controllers.habitacion_controller import router as habitacion_router
from controllers.reserva_controller import router as reserva_router
from controllers.dashboard_controller import router as dashboard_router
from controllers.factura_controller import router as factura_router
from controllers.usuario_controller import router as usuario_router

app = FastAPI(
    title="API de Reservas de Hotel",
    description="Backend para el sistema de reservas",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(habitacion_router)
app.include_router(reserva_router)
app.include_router(dashboard_router)
app.include_router(factura_router)
app.include_router(usuario_router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del Hotel. Visita /docs para ver la documentación."}