from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base
import uuid

class ReservaModel(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    
    habitacion_id: Mapped[int] = mapped_column(ForeignKey("habitaciones.id"))
    estado: Mapped[str] = mapped_column(String, default="pendiente")  # Estados: pendiente, pagado, cancelada