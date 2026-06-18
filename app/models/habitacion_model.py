from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base
class HabitacionModel(Base):
    __tablename__ = "habitaciones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, index=True)
    tipo = Column(String)
    precio = Column(Integer)
    disponible = Column(Boolean, default=True)