from pydantic import BaseModel
from uuid import UUID  #

class ReservaBase(BaseModel):
    usuario_id: UUID 
    habitacion_id: int
    estado: str

class ReservaResponse(ReservaBase):
    id: int

    class Config:
        from_attributes = True