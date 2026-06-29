"""
Pruebas unitarias para AuthService.

Verifica la autenticación de usuarios existentes y el rechazo
de registros con correo duplicado, aislando la lógica del servicio
mediante mocks del repositorio y de las funciones de seguridad.
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from models.user_model import UserModel
from models.user_schema import UserLogin, UserCreate, Role
from services.auth_service import AuthService

# Quitamos el @pytest.mark.asyncio de la clase, y lo pondremos en los métodos si es necesario
# Pero como usamos pytest-asyncio moderno, a veces basta con que la función sea async def.
# Lo ponemos explícito por si acaso.

class TestAuthService:
    """Pruebas del servicio de autenticación: login y registro."""

    @pytest.mark.asyncio
    @patch("services.auth_service.UserRepository")
    @patch("services.auth_service.verify_password")
    @patch("services.auth_service.create_access_token")
    async def test_authenticate_user_exitoso(self, mock_create_token, mock_verify_password, MockUserRepository):
        """Comprueba que authenticate_user devuelve un Token válido cuando las credenciales son correctas."""
        # 1. Preparar (Arrange)
        mock_repo_instance = MockUserRepository.return_value
        
        # Simulamos un usuario en la BD
        usuario_simulado = UserModel(email="admin@hotel.com", hashed_password="hashed", role=Role.USER)
        mock_repo_instance.get_user_by_email = AsyncMock(return_value=usuario_simulado)
        
        # Simulamos que la contraseña es correcta y que se genera un token
        mock_verify_password.return_value = True
        mock_create_token.return_value = "token_super_seguro_123"
        
        db_mock = AsyncMock()
        service = AuthService(db_mock)
        credenciales = UserLogin(email="admin@hotel.com", password="mi_password")

        # 2. Ejecutar (Act)
        resultado = await service.authenticate_user(credenciales)

        # 3. Comprobar (Assert)
        assert resultado.access_token == "token_super_seguro_123"
        assert resultado.token_type == "bearer"
        mock_repo_instance.get_user_by_email.assert_called_once_with("admin@hotel.com")


    @pytest.mark.asyncio
    @patch("services.auth_service.UserRepository")
    async def test_register_user_conflicto(self, MockUserRepository):
        """Verifica que register_user lanza HTTPException 409 si el correo ya está registrado."""
        # 1. Preparar (Arrange)
        mock_repo_instance = MockUserRepository.return_value
        
        # Simulamos que el correo YA existe en la base de datos
        usuario_simulado = UserModel(email="duplicado@hotel.com")
        mock_repo_instance.get_user_by_email = AsyncMock(return_value=usuario_simulado)
        
        db_mock = AsyncMock()
        service = AuthService(db_mock)
        datos = UserCreate(email="duplicado@hotel.com", password="password123")

        # 2 & 3. Ejecutar y Comprobar (Act & Assert)
        # Verificamos que lance el error de conflicto (HTTP 409)
        with pytest.raises(HTTPException) as info_error:
            await service.register_user(datos)
            
        assert info_error.value.status_code == 409
        assert info_error.value.detail == "Ya existe una cuenta con ese correo"