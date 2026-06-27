import pytest
import uuid
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.models.user_schema import PasswordChange
from services.usuario_service import usuario_service
from models.user_model import UserModel

# Usamos este decorador porque nuestras funciones son asíncronas
@pytest.mark.asyncio
class TestUsuarioService:

    @patch("services.usuario_service.UserRepository")
    async def test_obtener_perfil_exitoso(self, MockUserRepository):
        # 1. Preparar el escenario (Arrange)
        mock_repo_instance = MockUserRepository.return_value
        
        # Simulamos que la base de datos devuelve un usuario
        usuario_simulado = UserModel(id=uuid.uuid4(), email="test@correo.com", hashed_password="hashed123")
        mock_repo_instance.get_user_by_email = AsyncMock(return_value=usuario_simulado)
        
        mock_db = AsyncMock() # Simulamos la sesión de la BD

        # 2. Ejecutar la acción (Act)
        resultado = await usuario_service.obtener_perfil(mock_db, "test@correo.com")

        # 3. Comprobar los resultados (Assert)
        assert resultado is not None
        assert resultado.email == "test@correo.com"
        # Verificamos que el repositorio fue llamado exactamente con el email correcto
        mock_repo_instance.get_user_by_email.assert_called_once_with("test@correo.com")

    @patch("services.usuario_service.UserRepository")
    async def test_eliminar_usuario_propio_falla(self, MockUserRepository):
        # 1. Preparar el escenario (Arrange)
        mock_repo_instance = MockUserRepository.return_value
        
        usuario_id = uuid.uuid4()
        email_admin = "admin@correo.com"
        
        # Simulamos que el usuario que intentamos borrar ES el mismo administrador
        usuario_simulado = UserModel(id=usuario_id, email=email_admin)
        mock_repo_instance.get_user_by_id = AsyncMock(return_value=usuario_simulado)
        
        mock_db = AsyncMock()

        # 2 & 3. Ejecutar y Comprobar (Act & Assert)
        # Verificamos que el servicio lance el error HTTP 400 correcto
        with pytest.raises(HTTPException) as info_error:
            await usuario_service.eliminar_usuario(mock_db, usuario_id, email_admin)
        
        assert info_error.value.status_code == 400
        assert info_error.value.detail == "No puedes eliminar tu propia cuenta"