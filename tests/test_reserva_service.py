import pytest
import uuid
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

from models.reserva_schema import ReservaCreate
from services.reserva_service import reserva_service

class TestReservaService:

    @pytest.mark.asyncio
    @patch("services.reserva_service.reserva_repo")
    async def test_crear_reserva_exitosa(self, mock_reserva_repo):
        # 1. Preparar
        usuario_id = uuid.uuid4()
        datos = ReservaCreate(
            habitacion_id=1,
            fecha_checkin=date.today(),
            fecha_checkout=date.today() + timedelta(days=2)
        )
        
        # Simulamos que el repo crea la reserva correctamente
        mock_reserva_repo.crear = AsyncMock(return_value={"id": 1, "estado": "pendiente"})
        db_mock = AsyncMock()

        # 2. Ejecutar
        resultado = await reserva_service.crear_reserva(db_mock, datos, usuario_id)

        # 3. Comprobar
        assert resultado is not None
        assert resultado["id"] == 1
        mock_reserva_repo.crear.assert_called_once_with(db_mock, datos, usuario_id)

    @pytest.mark.asyncio
    @patch("services.reserva_service.reserva_repo")
    @patch("services.reserva_service.factura_repo")
    async def test_marcar_pagado_crea_factura(self, mock_factura_repo, mock_reserva_repo):
        # 1. Preparar: Simulamos la reserva que vamos a pagar
        mock_reserva = AsyncMock()
        mock_reserva.id = 100
        mock_reserva.usuario_id = uuid.uuid4()
        mock_reserva.costo_total = 250

        mock_reserva_repo.marcar_pagado = AsyncMock(return_value=mock_reserva)
        
        # Simulamos que NO hay factura previa para que intente crearla
        mock_factura_repo.obtener_por_reserva = AsyncMock(return_value=None)
        mock_factura_repo.crear = AsyncMock()
        
        db_mock = AsyncMock()

        # 2. Ejecutar
        resultado = await reserva_service.marcar_pagado(db_mock, 100)

        # 3. Comprobar: Aseguramos que se llamó al repo de facturas para crearla
        assert resultado is not None
        mock_factura_repo.crear.assert_called_once_with(
            db_mock, 100, mock_reserva.usuario_id, 250
        )