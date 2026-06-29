"""
Pruebas de integración para el controlador de autenticación (AuthController).

Cubre los endpoints POST /api/auth/login y POST /api/auth/registro,
usando TestClient de FastAPI y mocks del servicio para aislar la capa HTTP.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from main import app
from models.user_schema import Token

# Cliente de pruebas para la API
client = TestClient(app)

class TestAuthController:
    """Pruebas del controlador de autenticación: login y registro de usuarios."""

    @patch("controllers.auth_controller.AuthService")
    def test_login_exitoso(self, MockAuthService):
        """Verifica que un login con credenciales válidas devuelve 200 y el token de acceso."""
        # 1. Preparar el escenario
        mock_service_instance = MockAuthService.return_value
        
        # Simulamos que el servicio nos devuelve un Token válido
        mock_token = Token(access_token="super_token_secreto", token_type="bearer")
        mock_service_instance.authenticate_user = AsyncMock(return_value=mock_token)

        # 2. Ejecutar la acción
        # ¡OJO AQUI! Para OAuth2PasswordRequestForm enviamos 'data' (formulario), no 'json'
        response = client.post(
            "/api/auth/login",
            data={"username": "admin@hotel.com", "password": "MiPassword123"}
        )

        # 3. Comprobar resultados
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "super_token_secreto"
        assert data["token_type"] == "bearer"
        mock_service_instance.authenticate_user.assert_called_once()

    @patch("controllers.auth_controller.AuthService")
    def test_registro_exitoso(self, MockAuthService):
        """Verifica que el registro de un nuevo usuario devuelve 201 y el token generado."""
        # 1. Preparar el escenario
        mock_service_instance = MockAuthService.return_value
        
        mock_token = Token(access_token="token_nuevo_usuario", token_type="bearer")
        mock_service_instance.register_user = AsyncMock(return_value=mock_token)

        # 2. Ejecutar la acción
        # Para el registro (UserCreate), enviamos 'json' normal
        response = client.post(
            "/api/auth/registro",
            json={"email": "nuevo@hotel.com", "password": "Segura123"}
        )

        # 3. Comprobar resultados
        # Validamos que devuelva el status 201 Created que definiste en tu ruta
        assert response.status_code == 201
        data = response.json()
        assert data["access_token"] == "token_nuevo_usuario"
        mock_service_instance.register_user.assert_called_once()