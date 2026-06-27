from pydantic import BaseModel, ConfigDict

class HabitacionBase(BaseModel):
    numero: str
    tipo: str
    precio: int
    disponible: bool = True

class HabitacionCreate(HabitacionBase):
    pass

class HabitacionResponse(HabitacionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)