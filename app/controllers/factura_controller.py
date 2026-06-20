from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.user_schema import Role
from controllers.dependencies import get_current_user_token, require_role
from models.factura_schema import FacturaResponse
from services.factura_service import factura_service

router = APIRouter(prefix="/api/facturas", tags=["Facturas"])

@router.get("/", response_model=list[FacturaResponse])
async def listar_facturas(
    db: AsyncSession = Depends(get_db),
    admin: dict = Depends(require_role(Role.ADMIN))
):
    return await factura_service.listar_todas(db)

@router.get("/{reserva_id}", response_model=FacturaResponse)
async def obtener_factura(
    reserva_id: int,
    db: AsyncSession = Depends(get_db),
    usuario_actual: dict = Depends(get_current_user_token)
):
    factura = await factura_service.obtener_por_reserva(db, reserva_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura
