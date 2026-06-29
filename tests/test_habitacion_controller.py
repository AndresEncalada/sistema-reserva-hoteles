"""
Pruebas de integración para el controlador de habitaciones (HabitacionController).

Verifica que el listado de habitaciones es accesible públicamente y que
la modificación de estado requiere autenticación de administrador (401/403).
"""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock

from main import app
from services.habitacion_service import habitacion_service

@pytest.mark.asyncio
async def test_listar_habitaciones_publico():
    """
    Prueba que se puedan listar las habitaciones (ruta pública).
    Usamos un AsyncMock para simular la base de datos y evitar el error de conexión.
    """
    # Guardamos la función original para no dañar nada
    original_listar = habitacion_service.listar_habitaciones
    
    # Sobrescribimos temporalmente con un simulacro que devuelve una lista vacía
    habitacion_service.listar_habitaciones = AsyncMock(return_value=[])
    
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/habitaciones/")
            
            # Como es pública y no usa token, ahora esperamos un 200 OK exitoso
            assert response.status_code == 200
    finally:
        # Restauramos la función original
        habitacion_service.listar_habitaciones = original_listar

@pytest.mark.asyncio
async def test_cambiar_estado_sin_token():
    """
    Prueba que no se pueda modificar una habitación sin ser admin.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Intentamos cambiar el estado de la habitación 1
        response = await ac.patch("/api/habitaciones/1/estado?disponible=false")
        
        # Aceptamos tanto 401 (No autenticado) como 403 (Prohibido)
        assert response.status_code in [401, 403]