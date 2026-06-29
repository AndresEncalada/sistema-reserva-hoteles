import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.factura_repo import factura_repo

class FacturaService:
    """
    Servicio para la gestión de facturas.

    Orquesta las operaciones sobre facturas delegando al repositorio.

    Ejemplo de uso (Doctest):
    >>> from services.factura_service import FacturaService
    >>> servicio = FacturaService()
    >>> servicio is not None
    True
    >>> callable(servicio.listar_todas)
    True
    >>> callable(servicio.obtener_por_reserva)
    True
    >>> callable(servicio.crear)
    True
    """

    async def obtener_por_reserva(self, db: AsyncSession, reserva_id: int):
        """
        Obtiene la factura asociada a una reserva por su ID.

        Parámetros:
            db: Sesión de base de datos asíncrona.
            reserva_id: Identificador numérico de la reserva.

        Retorna:
            FacturaModel si existe, None si no se encontró ninguna factura.

        Ejemplo de uso (Doctest):
        >>> from services.factura_service import FacturaService
        >>> servicio = FacturaService()
        >>> hasattr(servicio, 'obtener_por_reserva')
        True
        """
        return await factura_repo.obtener_por_reserva(db, reserva_id)

    async def listar_todas(self, db: AsyncSession):
        """
        Retorna todas las facturas registradas en el sistema.

        Parámetros:
            db: Sesión de base de datos asíncrona.

        Retorna:
            Lista de FacturaModel (puede ser vacía si no hay facturas).

        Ejemplo de uso (Doctest):
        >>> from services.factura_service import FacturaService
        >>> servicio = FacturaService()
        >>> hasattr(servicio, 'listar_todas')
        True
        """
        return await factura_repo.listar_todas(db)

    async def crear(self, db: AsyncSession, reserva_id: int, usuario_id: uuid.UUID, monto: int):
        """
        Crea una nueva factura vinculada a una reserva pagada.

        Parámetros:
            db: Sesión de base de datos asíncrona.
            reserva_id: ID de la reserva a la que corresponde la factura.
            usuario_id: UUID del usuario propietario de la reserva.
            monto: Importe total en enteros (sin decimales).

        Retorna:
            FacturaModel recién creado con fecha de emisión del día actual.

        Ejemplo de uso (Doctest):
        >>> from services.factura_service import FacturaService
        >>> import uuid
        >>> servicio = FacturaService()
        >>> hasattr(servicio, 'crear')
        True
        >>> isinstance(uuid.uuid4(), uuid.UUID)
        True
        """
        return await factura_repo.crear(db, reserva_id, usuario_id, monto)

factura_service = FacturaService()
