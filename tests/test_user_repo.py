"""
Pruebas unitarias para UserRepository.

Verifica que el repositorio de usuarios consulta la base de datos
correctamente al buscar por email y al listar todos los usuarios.
"""
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from models.user_model import UserModel
from repositories.user_repo import UserRepository

@pytest.mark.asyncio
class TestUserRepository:
    """Pruebas del repositorio de usuarios: búsqueda por email y listado completo."""

    async def test_get_user_by_email(self):
        """Verifica que get_user_by_email retorna el usuario correcto cuando existe en la BD."""
        # 1. Preparar: Simulamos la base de datos
        mock_db = AsyncMock()
        mock_resultado = MagicMock()
        
        # Creamos un usuario falso
        usuario_simulado = UserModel(id=uuid.uuid4(), email="admin@hotel.com", hashed_password="123")
        
        # Configuramos la respuesta de la BD (simulando db.execute(...).scalar_one_or_none())
        mock_resultado.scalar_one_or_none.return_value = usuario_simulado
        mock_db.execute = AsyncMock(return_value=mock_resultado)
        
        repo = UserRepository(mock_db)

        # 2. Ejecutar
        resultado = await repo.get_user_by_email("admin@hotel.com")

        # 3. Comprobar
        assert resultado is not None
        assert resultado.email == "admin@hotel.com"
        mock_db.execute.assert_called_once()

    async def test_listar_todos(self):
        """Verifica que listar_todos devuelve todos los usuarios almacenados en la BD."""
        # 1. Preparar
        mock_db = AsyncMock()
        mock_resultado = MagicMock()
        
        # Simulamos una lista de usuarios
        lista_usuarios = [UserModel(email="uno@hotel.com"), UserModel(email="dos@hotel.com")]
        
        # Simulamos db.execute(...).scalars().all()
        mock_resultado.scalars().all.return_value = lista_usuarios
        mock_db.execute = AsyncMock(return_value=mock_resultado)
        
        repo = UserRepository(mock_db)

        # 2. Ejecutar
        resultado = await repo.listar_todos()

        # 3. Comprobar
        assert len(resultado) == 2
        assert resultado[0].email == "uno@hotel.com"