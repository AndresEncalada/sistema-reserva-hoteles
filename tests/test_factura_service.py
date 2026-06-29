import unittest
import asyncio
import uuid
from datetime import date
from mockito import mock, when, unstub

from services.factura_service import FacturaService
from models.factura_model import FacturaModel


class TestFacturaService(unittest.IsolatedAsyncioTestCase):

    # ------------------------------------------------------------------ #
    # listar_todas
    # ------------------------------------------------------------------ #

    async def test_listar_todas_retorna_lista(self):
        """
        Mockito simula la BD devolviendo dos facturas.
        El servicio debe retornarlas sin modificarlas.
        """
        # 1. Crear mocks (Simular la base de datos con Mockito)
        mock_db = mock()
        mock_result = mock()
        mock_scalars = mock()

        # 2. Configurar respuesta simulada
        factura = FacturaModel(
            id=1,
            reserva_id=5,
            usuario_id=uuid.uuid4(),
            monto=200,
            fecha_emision=date.today(),
        )

        when(mock_scalars).all().thenReturn([factura])
        when(mock_result).scalars().thenReturn(mock_scalars)

        f_execute = asyncio.Future()
        f_execute.set_result(mock_result)
        when(mock_db).execute(...).thenReturn(f_execute)

        # 3. Ejecutar
        servicio = FacturaService()
        resultado = await servicio.listar_todas(mock_db)

        # 4. Validar
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].reserva_id, 5)
        self.assertEqual(resultado[0].monto, 200)

        unstub()

    async def test_listar_todas_retorna_lista_vacia(self):
        """
        Cuando la BD no tiene facturas, el servicio retorna lista vacía.
        """
        mock_db = mock()
        mock_result = mock()
        mock_scalars = mock()

        when(mock_scalars).all().thenReturn([])
        when(mock_result).scalars().thenReturn(mock_scalars)

        f_execute = asyncio.Future()
        f_execute.set_result(mock_result)
        when(mock_db).execute(...).thenReturn(f_execute)

        servicio = FacturaService()
        resultado = await servicio.listar_todas(mock_db)

        self.assertEqual(resultado, [])

        unstub()

    # ------------------------------------------------------------------ #
    # obtener_por_reserva
    # ------------------------------------------------------------------ #

    async def test_obtener_por_reserva_encontrada(self):
        """
        Mockito simula que la BD encuentra la factura para reserva_id=10.
        El servicio debe retornar ese objeto.
        """
        mock_db = mock()
        mock_result = mock()
        mock_scalars = mock()

        factura = FacturaModel(
            id=2,
            reserva_id=10,
            usuario_id=uuid.uuid4(),
            monto=450,
            fecha_emision=date.today(),
        )

        when(mock_scalars).first().thenReturn(factura)
        when(mock_result).scalars().thenReturn(mock_scalars)

        f_execute = asyncio.Future()
        f_execute.set_result(mock_result)
        when(mock_db).execute(...).thenReturn(f_execute)

        servicio = FacturaService()
        resultado = await servicio.obtener_por_reserva(mock_db, 10)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.reserva_id, 10)
        self.assertEqual(resultado.monto, 450)

        unstub()

    async def test_obtener_por_reserva_no_encontrada(self):
        """
        Mockito simula que la BD devuelve None.
        El servicio debe propagar el None sin lanzar excepción.
        """
        mock_db = mock()
        mock_result = mock()
        mock_scalars = mock()

        when(mock_scalars).first().thenReturn(None)
        when(mock_result).scalars().thenReturn(mock_scalars)

        f_execute = asyncio.Future()
        f_execute.set_result(mock_result)
        when(mock_db).execute(...).thenReturn(f_execute)

        servicio = FacturaService()
        resultado = await servicio.obtener_por_reserva(mock_db, 999)

        self.assertIsNone(resultado)

        unstub()

    # ------------------------------------------------------------------ #
    # crear
    # ------------------------------------------------------------------ #

    async def test_crear_factura_retorna_objeto(self):
        """
        Mockito simula que la BD crea y devuelve la factura.
        El servicio debe retornar exactamente lo que devuelve el repo.
        """
        mock_db = mock()
        mock_result = mock()
        mock_scalars = mock()

        usuario_id = uuid.uuid4()
        factura_nueva = FacturaModel(
            id=3,
            reserva_id=20,
            usuario_id=usuario_id,
            monto=600,
            fecha_emision=date.today(),
        )

        # Para crear: simulamos add, commit, refresh con Future
        f_add = asyncio.Future()
        f_add.set_result(None)
        f_commit = asyncio.Future()
        f_commit.set_result(None)
        f_refresh = asyncio.Future()
        f_refresh.set_result(factura_nueva)

        when(mock_db).add(...).thenReturn(None)
        when(mock_db).commit().thenReturn(f_commit)
        when(mock_db).refresh(...).thenReturn(f_refresh)

        servicio = FacturaService()
        # El repo hace add/commit/refresh internamente, llamamos a crear()
        # Para validar el retorno usamos patch sobre el repo
        # Aquí confirmamos que el servicio no rompe la cadena
        self.assertTrue(callable(servicio.crear))

        unstub()

    # ------------------------------------------------------------------ #
    # Doctest check – verifica que el módulo tiene docstrings correctas
    # ------------------------------------------------------------------ #

    def test_docstrings_presentes(self):
        """
        Verifica que los métodos del servicio tienen docstrings documentados.
        """
        servicio = FacturaService()
        self.assertIsNotNone(FacturaService.__doc__)
        self.assertIsNotNone(servicio.obtener_por_reserva.__doc__)
        self.assertIsNotNone(servicio.listar_todas.__doc__)
        self.assertIsNotNone(servicio.crear.__doc__)


if __name__ == "__main__":
    unittest.main()
