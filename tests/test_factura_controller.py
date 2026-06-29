"""
Pruebas de integración para el controlador de facturas (FacturaController).

Cubre el listado de facturas (solo admin) y la consulta de factura por reserva,
verificando control de acceso por roles (admin/user/sin token) mediante
dependency_overrides de FastAPI y mocks del servicio.
"""
import pytest
import uuid
from datetime import date
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from main import app
from controllers.dependencies import get_current_user_token
from models.factura_schema import FacturaResponse

client = TestClient(app)


# ------------------------------------------------------------------ #
# Helpers de autenticación simulada
# ------------------------------------------------------------------ #

async def mock_admin():
    return {"email": "admin@hotel.com", "role": "admin"}


async def mock_usuario():
    return {"email": "cliente@hotel.com", "role": "user"}


def _factura_ejemplo(reserva_id: int = 5, monto: int = 300) -> FacturaResponse:
    return FacturaResponse(
        id=1,
        reserva_id=reserva_id,
        usuario_id=uuid.uuid4(),
        monto=monto,
        fecha_emision=date.today(),
    )


# ================================================================== #
# GET /api/facturas/  — listado completo (solo admin)
# ================================================================== #

class TestListarFacturas:

    def setup_method(self):
        # Guardamos el estado actual de overrides para no interferir
        # con los overrides globales de otros archivos de test.
        self._saved_overrides = dict(app.dependency_overrides)

    def teardown_method(self):
        # Restauramos exactamente el estado anterior.
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self._saved_overrides)

    @patch("controllers.factura_controller.factura_service")
    def test_admin_puede_listar_facturas(self, mock_factura_service):
        """
        Un admin autenticado recibe 200 con la lista de facturas.
        Usamos patch para simular el servicio y dependency_overrides
        para inyectar el token de admin sin llamar a la BD.
        """
        app.dependency_overrides[get_current_user_token] = mock_admin
        mock_factura_service.listar_todas = AsyncMock(return_value=[_factura_ejemplo()])

        response = client.get("/api/facturas/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["reserva_id"] == 5
        assert data[0]["monto"] == 300

    @patch("controllers.factura_controller.factura_service")
    def test_admin_recibe_lista_vacia_si_no_hay_facturas(self, mock_factura_service):
        """
        Si no existen facturas, el admin recibe 200 con lista vacía.
        """
        app.dependency_overrides[get_current_user_token] = mock_admin
        mock_factura_service.listar_todas = AsyncMock(return_value=[])

        response = client.get("/api/facturas/")

        assert response.status_code == 200
        assert response.json() == []

    def test_listar_sin_token_retorna_401(self):
        """
        Sin token de autenticación la ruta debe retornar 401 Unauthorized.
        """
        app.dependency_overrides.pop(get_current_user_token, None)

        response = client.get("/api/facturas/")

        assert response.status_code == 401

    def test_usuario_normal_no_puede_listar_retorna_403(self):
        """
        Un usuario con rol 'user' no puede listar todas las facturas.
        La ruta exige rol admin → 403 Forbidden.
        """
        app.dependency_overrides[get_current_user_token] = mock_usuario

        response = client.get("/api/facturas/")

        assert response.status_code == 403
        assert "permisos" in response.json()["detail"].lower()


# ================================================================== #
# GET /api/facturas/{reserva_id}  — factura por reserva
# ================================================================== #

class TestObtenerFactura:

    def setup_method(self):
        self._saved_overrides = dict(app.dependency_overrides)

    def teardown_method(self):
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self._saved_overrides)

    @patch("controllers.factura_controller.factura_service")
    def test_usuario_autenticado_puede_consultar_factura(self, mock_factura_service):
        """
        Cualquier usuario autenticado puede consultar la factura de una reserva.
        Recibe 200 con los datos de la factura.
        """
        app.dependency_overrides[get_current_user_token] = mock_usuario
        mock_factura_service.obtener_por_reserva = AsyncMock(
            return_value=_factura_ejemplo(reserva_id=7, monto=450)
        )

        response = client.get("/api/facturas/7")

        assert response.status_code == 200
        data = response.json()
        assert data["reserva_id"] == 7
        assert data["monto"] == 450
        assert "fecha_emision" in data
        assert "usuario_id" in data

    @patch("controllers.factura_controller.factura_service")
    def test_admin_tambien_puede_consultar_factura(self, mock_factura_service):
        """
        Un admin también puede consultar la factura de una reserva.
        """
        app.dependency_overrides[get_current_user_token] = mock_admin
        mock_factura_service.obtener_por_reserva = AsyncMock(
            return_value=_factura_ejemplo(reserva_id=3, monto=150)
        )

        response = client.get("/api/facturas/3")

        assert response.status_code == 200
        assert response.json()["monto"] == 150

    @patch("controllers.factura_controller.factura_service")
    def test_factura_no_encontrada_retorna_404(self, mock_factura_service):
        """
        Si el servicio devuelve None, el controlador debe lanzar 404.
        """
        app.dependency_overrides[get_current_user_token] = mock_usuario
        mock_factura_service.obtener_por_reserva = AsyncMock(return_value=None)

        response = client.get("/api/facturas/999")

        assert response.status_code == 404
        assert response.json() == {"detail": "Factura no encontrada"}

    def test_consultar_factura_sin_token_retorna_401(self):
        """
        Sin autenticación la ruta retorna 401 Unauthorized.
        """
        app.dependency_overrides.pop(get_current_user_token, None)

        response = client.get("/api/facturas/1")

        assert response.status_code == 401
