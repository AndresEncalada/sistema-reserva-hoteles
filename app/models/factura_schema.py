from pydantic import BaseModel
from datetime import date
from uuid import UUID

class FacturaResponse(BaseModel):
    id: int
    reserva_id: int
    usuario_id: UUID
    monto: int
    fecha_emision: date

    class Config:
        from_attributes = True
