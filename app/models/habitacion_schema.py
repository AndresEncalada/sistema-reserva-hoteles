from pydantic import BaseModel

class HabitacionBase(BaseModel):
    numero: str
    tipo: str
    precio: int
    disponible: bool = True

class HabitacionCreate(HabitacionBase):
    pass

class HabitacionResponse(HabitacionBase):
    id: int

    class Config:
        from_attributes = True