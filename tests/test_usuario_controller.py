"""
Pruebas de integración para el controlador de usuarios (UsuarioController).

Verifica el endpoint GET /api/usuarios/me con usuario autenticado,
cubriendo los casos de perfil encontrado y perfil no encontrado (404).
"""
import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from main import app
from models.user_model import UserModel
from controllers.dependencies import get_current_user_token

# Creamos un cliente de pruebas para nuestra API
client = TestClient(app)

# Simulamos un usuario falso para que pase la autenticación
async def mock_get_current_user_token():
    return {"email": "test@correo.com", "role": "user"}

# Sobrescribimos la dependencia real por nuestra simulación
app.dependency_overrides[get_current_user_token] = mock_get_current_user_token

class TestUsuarioController:
    """Pruebas del controlador de usuarios: consulta del perfil propio."""

    @patch("controllers.usuario_controller.usuario_service")
    def test_obtener_perfil_exitoso(self, mock_usuario_service):
        """Verifica que GET /api/usuarios/me devuelve 200 con los datos del usuario autenticado."""
        # 1. Preparar el escenario: Simulamos lo que respondería el servicio
        usuario_simulado = {
            "id": str(uuid.uuid4()),
            "email": "test@correo.com",
            "role": "user"
        }
        # Como obtener_perfil es asíncrono, usamos AsyncMock
        mock_usuario_service.obtener_perfil = AsyncMock(return_value=usuario_simulado)

        # 2. Ejecutar la acción: Hacemos una petición GET a la ruta
        response = client.get("/api/usuarios/me")

        # 3. Comprobar los resultados
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@correo.com"
        assert "id" in data

    @patch("controllers.usuario_controller.usuario_service")
    def test_obtener_perfil_no_encontrado(self, mock_usuario_service):
        """Verifica que GET /api/usuarios/me devuelve 404 cuando el usuario no existe en la BD."""
        # 1. Preparar el escenario: Simulamos que el servicio devuelve None (usuario no existe)
        mock_usuario_service.obtener_perfil = AsyncMock(return_value=None)

        # 2. Ejecutar la acción
        response = client.get("/api/usuarios/me")

        # 3. Comprobar que nos lanza el error 404 que programaste en el controlador
        assert response.status_code == 404
        assert response.json() == {"detail": "Usuario no encontrado"}