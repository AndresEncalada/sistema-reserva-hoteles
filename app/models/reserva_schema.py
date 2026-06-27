from pydantic import BaseModel, ConfigDict, model_validator
from uuid import UUID
from datetime import date
from typing import Optional

class ReservaCreate(BaseModel):
    habitacion_id: int
    fecha_checkin: date
    fecha_checkout: date

    @model_validator(mode="after")
    def checkout_posterior_a_checkin(self):
        if self.fecha_checkout <= self.fecha_checkin:
            raise ValueError("fecha_checkout debe ser posterior a fecha_checkin")
        return self

class ReservaBase(BaseModel):
    usuario_id: UUID
    habitacion_id: int
    estado: str
    fecha_checkin: Optional[date] = None
    fecha_checkout: Optional[date] = None
    costo_total: Optional[int] = None

class ReservaResponse(ReservaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)