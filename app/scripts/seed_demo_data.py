import asyncio
import os
import sys
from datetime import date

from sqlalchemy import select

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

from core.database import AsyncSessionLocal
from core.security import get_password_hash
from models.factura_model import FacturaModel
from models.habitacion_model import HabitacionModel
from models.reserva_model import ReservaModel
from models.user_model import UserModel
from models.user_schema import Role


DEMO_USERS = [
    ("maria.gomez@hotel.com", "maria123", Role.USER),
    ("carlos.perez@hotel.com", "carlos123", Role.USER),
    ("ana.torres@hotel.com", "ana123", Role.USER),
    ("recepcion@hotel.com", "recepcion123", Role.ADMIN),
]

DEMO_ROOMS = [
    ("101", "Individual", 45, True),
    ("102", "Individual", 45, True),
    ("201", "Doble", 75, True),
    ("202", "Doble", 80, False),
    ("301", "Suite", 140, True),
    ("302", "Suite", 155, True),
    ("401", "Familiar", 120, True),
    ("402", "Familiar", 125, False),
]


async def get_or_create_user(db, email: str, password: str, role: Role) -> UserModel:
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if user:
        return user

    user = UserModel(
        email=email,
        hashed_password=get_password_hash(password),
        role=role,
    )
    db.add(user)
    await db.flush()
    return user


async def get_or_create_room(
    db,
    numero: str,
    tipo: str,
    precio: int,
    disponible: bool,
) -> HabitacionModel:
    result = await db.execute(select(HabitacionModel).where(HabitacionModel.numero == numero))
    room = result.scalar_one_or_none()
    if room:
        room.tipo = tipo
        room.precio = precio
        room.disponible = disponible
        return room

    room = HabitacionModel(
        numero=numero,
        tipo=tipo,
        precio=precio,
        disponible=disponible,
    )
    db.add(room)
    await db.flush()
    return room


async def reservation_exists(db, user_id, room_id: int, checkin: date, checkout: date) -> bool:
    result = await db.execute(
        select(ReservaModel).where(
            ReservaModel.usuario_id == user_id,
            ReservaModel.habitacion_id == room_id,
            ReservaModel.fecha_checkin == checkin,
            ReservaModel.fecha_checkout == checkout,
        )
    )
    return result.scalar_one_or_none() is not None


async def create_reservation(
    db,
    user: UserModel,
    room: HabitacionModel,
    estado: str,
    checkin: date,
    checkout: date,
) -> ReservaModel | None:
    if await reservation_exists(db, user.id, room.id, checkin, checkout):
        return None

    nights = (checkout - checkin).days
    reserva = ReservaModel(
        usuario_id=user.id,
        habitacion_id=room.id,
        estado=estado,
        fecha_checkin=checkin,
        fecha_checkout=checkout,
        costo_total=room.precio * nights,
    )
    db.add(reserva)
    await db.flush()
    return reserva


async def create_invoice_if_needed(db, reserva: ReservaModel) -> bool:
    result = await db.execute(select(FacturaModel).where(FacturaModel.reserva_id == reserva.id))
    if result.scalar_one_or_none():
        return False

    factura = FacturaModel(
        reserva_id=reserva.id,
        usuario_id=reserva.usuario_id,
        monto=reserva.costo_total or 0,
        fecha_emision=date.today(),
    )
    db.add(factura)
    return True


async def seed_demo_data():
    async with AsyncSessionLocal() as db:
        users = {}
        for email, password, role in DEMO_USERS:
            users[email] = await get_or_create_user(db, email, password, role)

        rooms = {}
        for numero, tipo, precio, disponible in DEMO_ROOMS:
            rooms[numero] = await get_or_create_room(db, numero, tipo, precio, disponible)

        reservations_to_create = [
            ("maria.gomez@hotel.com", "101", "pagado", date(2026, 7, 1), date(2026, 7, 4)),
            ("maria.gomez@hotel.com", "301", "pendiente", date(2026, 8, 10), date(2026, 8, 13)),
            ("carlos.perez@hotel.com", "201", "pagado", date(2026, 7, 5), date(2026, 7, 7)),
            ("carlos.perez@hotel.com", "401", "cancelada", date(2026, 9, 2), date(2026, 9, 6)),
            ("ana.torres@hotel.com", "302", "pendiente", date(2026, 7, 15), date(2026, 7, 18)),
            ("ana.torres@hotel.com", "102", "pagado", date(2026, 8, 20), date(2026, 8, 22)),
        ]

        created_reservations = 0
        created_invoices = 0
        for user_email, room_number, estado, checkin, checkout in reservations_to_create:
            reserva = await create_reservation(
                db,
                users[user_email],
                rooms[room_number],
                estado,
                checkin,
                checkout,
            )
            if not reserva:
                continue

            created_reservations += 1
            if estado == "pagado" and await create_invoice_if_needed(db, reserva):
                created_invoices += 1

        await db.commit()

        print("Datos demo cargados correctamente.")
        print(f"Usuarios demo disponibles: {len(DEMO_USERS)}")
        print(f"Habitaciones demo disponibles: {len(DEMO_ROOMS)}")
        print(f"Reservas nuevas creadas: {created_reservations}")
        print(f"Facturas nuevas creadas: {created_invoices}")


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
