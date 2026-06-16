# API Sistema de Reservas de Hotel

Este repositorio contiene el backend del sistema de reservas de hotel, construido con **FastAPI**. Actualmente, incluye la base de datos configurada, el entorno gestionado con `uv` y el **módulo de autenticación (Login y Roles)** completamente funcional.

## 1. Configuración del Entorno (Primeros Pasos)

Para evitar problemas de dependencias, utilizamos `uv` y contenedores para la base de datos. Ejecute los siguientes comandos en su terminal (asegúrese de tener Docker corriendo):

1. **Sincronizar el entorno de Python:**
   ```bash
   uv sync
   ```
2. **Levantar PostgreSQL:**
   ```bash
   docker compose up -d
   ```
3. **Crear las tablas en la base de datos:**
   ```bash
   uv run app/scripts/init_db.py
   ```
4. **Sembrar usuarios de prueba:**
   ```bash
   uv run app/scripts/seed_users.py
   ```
5. **Iniciar el servidor en modo desarrollo:**
   ```bash
   uv run uvicorn main:app --app-dir app --reload
   ```

> **Credenciales de prueba disponibles:**
> * **Administrador:** `admin@hotel.com` / `admin123`
> * **Huésped:** `huesped@hotel.com` / `huesped123`

---

## 2. Autenticación y Manejo de Roles (RBAC)

El sistema utiliza **JWT (JSON Web Tokens)**. Cuando un usuario hace login exitosamente, el servidor devuelve un token cifrado que contiene su `email` y su `rol` (`admin` o `user`). 

Para proteger los endpoints que se desarrollen (Dashboards, Reservas, etc.), **no necesita reescribir lógica de seguridad**. Solo deben usar las dependencias ya inyectables que se encuentran en `app/controllers/dependencies.py`.

### A. Endpoints para cualquier usuario logueado (Huéspedes y Admins)
Para extraer los datos del usuario autenticado, importe y use `get_current_user_token`.

```python
from fastapi import APIRouter, Depends
# Nota: Siempre usar importaciones absolutas desde 'app.'
from app.controllers.dependencies import get_current_user_token

router = APIRouter(prefix="/api/reservas")

@router.post("/crear")
async def crear_reserva(usuario: dict = Depends(get_current_user_token)):
    # La variable 'usuario' es un diccionario extraído del JWT
    correo_usuario = usuario["email"]
    rol_usuario = usuario["role"]
    
    return {"mensaje": f"Reserva iniciada para el correo: {correo_usuario}"}
```

### B. Endpoints Exclusivos para el Personal (Solo Admins)
Para los módulos de administración (Dashboards), use `require_role(Role.ADMIN)`. FastAPI se encargará automáticamente de bloquear (Error 403) a los huéspedes que intenten acceder.

```python
from fastapi import APIRouter, Depends
from app.models.user_schema import Role
from app.controllers.dependencies import require_role

router = APIRouter(prefix="/api/dashboard")

@router.get("/estadisticas")
async def ver_estadisticas(admin: dict = Depends(require_role(Role.ADMIN))):
    # Si el código llega aquí, está garantizado que el usuario es Admin
    return {"mensaje": f"Bienvenido al panel, administrador {admin['email']}"}
```

---

## 3. Pruebas Rápidas

No necesita Postman. FastAPI autogenera la documentación y la interfaz de pruebas:
1. Vayan a `http://127.0.0.1:8000/docs`.
2. Use el endpoint `POST /api/auth/login` con un usuario de prueba para obtener un `access_token`.
3. Haga clic en el botón superior **Authorize** (el ícono del candado) y pegue el token.
4. Pruebe sus propios endpoints directamente desde la página.

---

## 4. Contexto para LLMs (Claude Code / Agentes CLI)

> **[LLM_CONTEXT_START]**
> Este proyecto sigue una arquitectura Modelo-Repositorio-Servicio-Controlador (MRSC) en FastAPI asíncrono.
> * **Gestor de paquetes:** `uv`
> * **ORM:** SQLAlchemy 2.0 (asíncrono con `asyncpg`).
> * **Seguridad:** Autenticación sin estado (JWT) guardando email y rol en el payload. Hasheo de contraseñas con `bcrypt` (librería nativa, no passlib). Configuración cargada vía `pydantic-settings` desde `.env`.
> * **Modelos Base:** `UserModel` (PostgreSQL) y esquemas Pydantic en `app/models/`.
> 
> **Instrucciones para generar nuevos módulos:**
> 1. Al crear un nuevo recurso (ej. `Habitacion`), genera `habitacion_model.py`, `habitacion_schema.py`, `habitacion_repo.py`, `habitacion_service.py` y `habitacion_controller.py`.
> 2. Mantén la inyección de dependencias pasando `db: AsyncSession` desde el controlador al servicio y luego al repositorio.
> 3. Emplea `Depends(get_current_user_token)` o `Depends(require_role(Role.ADMIN))` en los controladores para acceder al usuario de la petición.
> 4. Asegúrate de añadir las importaciones de las nuevas tablas a `app/scripts/init_db.py` para que se generen al inicializar.
> **[LLM_CONTEXT_END]**