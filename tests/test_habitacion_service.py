"""
Pruebas unitarias para HabitacionService usando Mockito.

Verifica que el servicio de habitaciones consulta la base de datos
y retorna correctamente la lista de habitaciones disponibles.
"""
import unittest
import asyncio
from mockito import mock, when, unstub
from services.habitacion_service import HabitacionService
from models.habitacion_model import HabitacionModel

class TestHabitacionService(unittest.IsolatedAsyncioTestCase):
    """Pruebas del servicio de habitaciones: listado con BD simulada via Mockito."""

    async def test_listar_habitaciones(self):
        """Verifica que listar_habitaciones devuelve las habitaciones que retorna la BD."""
        # 1. Crear mocks (Simular la base de datos)
        mock_db = mock()
        mock_result = mock()
        mock_scalars = mock()
        
        # 2. Configurar la respuesta simulada
        habitacion = HabitacionModel(id=1, numero="101", tipo="Sencilla", precio=50, disponible=True)
        
        when(mock_scalars).all().thenReturn([habitacion])
        when(mock_result).scalars().thenReturn(mock_scalars)
        
        # Truco para simular funciones asíncronas con Mockito en Python
        f_execute = asyncio.Future()
        f_execute.set_result(mock_result)
        when(mock_db).execute(...).thenReturn(f_execute)

        # 3. Ejecutar el servicio
        servicio = HabitacionService()
        resultado = await servicio.listar_habitaciones(mock_db)

        # 4. Validar
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].numero, "101")
        
        # Limpiar configuración de mockito
        unstub()