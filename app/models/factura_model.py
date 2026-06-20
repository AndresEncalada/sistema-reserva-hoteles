from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
from datetime import date
import uuid

class FacturaModel(Base):
    __tablename__ = "facturas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reserva_id: Mapped[int] = mapped_column(ForeignKey("reservas.id"), unique=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    monto: Mapped[int] = mapped_column(Integer)
    fecha_emision: Mapped[date] = mapped_column(Date)
