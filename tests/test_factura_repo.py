"""
Pruebas unitarias para el repositorio de facturas (factura_repo).

Cubre obtener_por_reserva, listar_todas y crear, verificando que
las operaciones de BD (execute, add, commit, refresh) se invocan
correctamente usando sesiones de BD simuladas con AsyncMock.
"""
import pytest
import uuid
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from models.factura_model import FacturaModel
from repositories.factura_repo import factura_repo


class TestFacturaRepo:

    # ------------------------------------------------------------------ #
    # obtener_por_reserva
    # ------------------------------------------------------------------ #

    @pytest.mark.asyncio
    async def test_obtener_por_reserva_encontrada(self):
        """
        Cuando existe una factura para la reserva indicada, el repo la retorna.
        Usamos AsyncMock para simular la sesión de base de datos.
        """
        mock_db = AsyncMock()
        mock_resultado = MagicMock()

        factura_simulada = FacturaModel(
            id=1,
            reserva_id=10,
            usuario_id=uuid.uuid4(),
            monto=300,
            fecha_emision=date.today(),
        )
        mock_resultado.scalars().first.return_value = factura_simulada
        mock_db.execute = AsyncMock(return_value=mock_resultado)

        resultado = await factura_repo.obtener_por_reserva(mock_db, 10)

        assert resultado is not None
        assert resultado.reserva_id == 10
        assert resultado.monto == 300
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_obtener_por_reserva_no_encontrada(self):
        """
        Cuando no existe factura para el reserva_id, el repo retorna None.
        """
        mock_db = AsyncMock()
        mock_resultado = MagicMock()
        mock_resultado.scalars().first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_resultado)

        resultado = await factura_repo.obtener_por_reserva(mock_db, 999)

        assert resultado is None
        mock_db.execute.assert_called_once()

    # ------------------------------------------------------------------ #
    # listar_todas
    # ------------------------------------------------------------------ #

    @pytest.mark.asyncio
    async def test_listar_todas_con_facturas(self):
        """
        Cuando hay facturas, el repo devuelve la lista completa.
        """
        mock_db = AsyncMock()
        mock_resultado = MagicMock()

        lista_simulada = [
            FacturaModel(id=1, reserva_id=1, monto=100),
            FacturaModel(id=2, reserva_id=2, monto=200),
        ]
        mock_resultado.scalars().all.return_value = lista_simulada
        mock_db.execute = AsyncMock(return_value=mock_resultado)

        resultado = await factura_repo.listar_todas(mock_db)

        assert len(resultado) == 2
        assert resultado[0].monto == 100
        assert resultado[1].monto == 200
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_listar_todas_sin_facturas(self):
        """
        Cuando no hay facturas, el repo devuelve una lista vacía.
        """
        mock_db = AsyncMock()
        mock_resultado = MagicMock()
        mock_resultado.scalars().all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_resultado)

        resultado = await factura_repo.listar_todas(mock_db)

        assert resultado == []
        mock_db.execute.assert_called_once()

    # ------------------------------------------------------------------ #
    # crear
    # ------------------------------------------------------------------ #

    @pytest.mark.asyncio
    async def test_crear_factura_llama_operaciones_db(self):
        """
        Al crear una factura, el repo debe llamar a add(), commit() y refresh()
        con los datos correctos.
        """
        mock_db = AsyncMock()
        usuario_id = uuid.uuid4()

        await factura_repo.crear(mock_db, reserva_id=5, usuario_id=usuario_id, monto=500)

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_crear_factura_campos_correctos(self):
        """
        El objeto FacturaModel que se añade a la BD debe tener
        los campos exactos que recibió el repo.
        """
        mock_db = AsyncMock()
        usuario_id = uuid.uuid4()

        await factura_repo.crear(mock_db, reserva_id=7, usuario_id=usuario_id, monto=750)

        # El primer argumento de db.add() es el objeto que se va a guardar
        factura_guardada = mock_db.add.call_args[0][0]
        assert isinstance(factura_guardada, FacturaModel)
        assert factura_guardada.reserva_id == 7
        assert factura_guardada.usuario_id == usuario_id
        assert factura_guardada.monto == 750
        assert factura_guardada.fecha_emision == date.today()
