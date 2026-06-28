import pytest
import uuid
from datetime import date, timedelta
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from main import app
from controllers.dependencies import get_current_user_token

client = TestClient(app)

# Simulamos la autenticación
async def mock_get_current_user_token():
    return {"email": "cliente@hotel.com", "role": "user"}

app.dependency_overrides[get_current_user_token] = mock_get_current_user_token

class TestReservaController:

    @patch("controllers.reserva_controller.UserRepository")
    @patch("controllers.reserva_controller.reserva_service")
    def test_crear_reserva_exitosa(self, mock_reserva_service, MockUserRepository):
        # 1. Preparar Usuario Simulado
        mock_user_repo_instance = MockUserRepository.return_value
        mock_user = AsyncMock()
        mock_user.id = uuid.uuid4()
        mock_user_repo_instance.get_user_by_email = AsyncMock(return_value=mock_user)

        # 2. Preparar Reserva Simulada
        reserva_simulada = {
            "id": 1,
            "usuario_id": str(mock_user.id),
            "habitacion_id": 1,
            "estado": "pendiente",
            "fecha_checkin": str(date.today()),
            "fecha_checkout": str(date.today() + timedelta(days=2)),
            "costo_total": 200
        }
        mock_reserva_service.crear_reserva = AsyncMock(return_value=reserva_simulada)

        # 3. Ejecutar Petición
        response = client.post(
            "/api/reservas/",
            json={
                "habitacion_id": 1,
                "fecha_checkin": str(date.today()),
                "fecha_checkout": str(date.today() + timedelta(days=2))
            }
        )

        # 4. Comprobar
        assert response.status_code == 201
        data = response.json()
        assert data["estado"] == "pendiente"
        assert data["id"] == 1
        assert data["costo_total"] == 200

    @patch("controllers.reserva_controller.reserva_service")
    def test_notificar_pago_no_encontrado(self, mock_reserva_service):
        # Simulamos que la reserva no existe (devuelve None)
        mock_reserva_service.enviar_notificacion_pago = AsyncMock(return_value=None)

        response = client.post("/api/reservas/999/notificar-pago")

        # Comprobamos que lance el error 404 que programaste
        assert response.status_code == 404
        assert response.json() == {"detail": "Reserva no encontrada"}