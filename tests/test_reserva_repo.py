import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from models.reserva_model import ReservaModel
from repositories.reserva_repo import reserva_repo

class TestReservaRepo:

    @pytest.mark.asyncio
    async def test_obtener_por_id(self):
        # 1. Preparar la BD simulada
        mock_db = AsyncMock()
        mock_resultado = MagicMock()
        
        # Simulamos que la BD devuelve una reserva con ID 15
        reserva_simulada = ReservaModel(id=15, estado="pendiente")
        mock_resultado.scalars().first.return_value = reserva_simulada
        mock_db.execute = AsyncMock(return_value=mock_resultado)
        
        # 2. Ejecutar
        resultado = await reserva_repo.obtener_por_id(mock_db, 15)
        
        # 3. Comprobar
        assert resultado is not None
        assert resultado.id == 15
        assert resultado.estado == "pendiente"
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_listar_todas(self):
        # 1. Preparar la BD simulada
        mock_db = AsyncMock()
        mock_resultado = MagicMock()
        
        # Simulamos una lista de reservas
        lista_simulada = [ReservaModel(id=1), ReservaModel(id=2)]
        mock_resultado.scalars().all.return_value = lista_simulada
        mock_db.execute = AsyncMock(return_value=mock_resultado)
        
        # 2. Ejecutar
        resultado = await reserva_repo.listar_todas(mock_db)
        
        # 3. Comprobar
        assert len(resultado) == 2
        mock_db.execute.assert_called_once()