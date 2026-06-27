from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID

class FacturaResponse(BaseModel):
    id: int
    reserva_id: int
    usuario_id: UUID
    monto: int
    fecha_emision: date
    model_config = ConfigDict(from_attributes=True)
