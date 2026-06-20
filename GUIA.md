# Guía de Uso — API Sistema de Reservas de Hotel

Esta guía explica paso a paso cómo configurar, ejecutar y probar todos los endpoints del sistema.

---

## ⚠️ Cambios recientes en la base de datos

> **Leer esto antes de ejecutar el proyecto.**

Se realizaron cambios en la estructura de la base de datos que requieren acciones distintas dependiendo de tu situación:

---

### Caso A — Primera vez que ejecutas el proyecto

No necesitas hacer nada especial. Al correr `uv run app/scripts/init_db.py` en el paso de configuración inicial, todas las tablas se crean correctamente con la estructura más reciente.

Sigue directo a la sección **2. Configuración inicial**.

---

### Caso B — Ya tenías el proyecto corriendo antes de estos cambios

Se agregaron columnas nuevas a la tabla `reservas` y se creó una tabla nueva `facturas`. Debes aplicar los siguientes comandos **con el servidor detenido**:

**Paso 1 — Agregar columnas nuevas a la tabla `reservas`:**
```bash
docker exec sistema-reserva-hoteles-db-1 psql -U hotel_user -d hotel_reservations -c "ALTER TABLE reservas ADD COLUMN IF NOT EXISTS fecha_checkin DATE; ALTER TABLE reservas ADD COLUMN IF NOT EXISTS fecha_checkout DATE; ALTER TABLE reservas ADD COLUMN IF NOT EXISTS costo_total INTEGER;"
```

**Paso 2 — Crear la tabla `facturas`:**
```bash
uv run app/scripts/init_db.py
```
> `init_db.py` usa `CREATE TABLE IF NOT EXISTS`, por lo que no borra datos existentes — solo crea lo que falta.

**Paso 3 — Volver a levantar el servidor:**
```bash
uv run uvicorn main:app --app-dir app --reload
```

---

### Resumen de cambios estructurales

| Tabla | Cambio | Descripción |
|---|---|---|
| `reservas` | Nueva columna `fecha_checkin` | Fecha de entrada (tipo DATE) |
| `reservas` | Nueva columna `fecha_checkout` | Fecha de salida (tipo DATE) |
| `reservas` | Nueva columna `costo_total` | Precio × noches, calculado automáticamente |
| `facturas` | **Tabla nueva** | Se genera automáticamente al pagar una reserva |

---

## 1. Requisitos previos

Tener instalado en el equipo:
- [Docker](https://www.docker.com/) (para la base de datos)
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes de Python)

Si `uv` no está instalado, ejecutar:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 2. Configuración inicial (solo la primera vez)

Ejecutar los siguientes comandos en orden desde la carpeta raíz del proyecto:

```bash
# 1. Instalar dependencias de Python
uv sync

# 2. Levantar la base de datos PostgreSQL
docker compose up -d

# 3. Crear las tablas en la base de datos
uv run app/scripts/init_db.py

# 4. Crear los usuarios de prueba
uv run app/scripts/seed_users.py
```

---

## 3. Iniciar el servidor

```bash
uv run uvicorn main:app --app-dir app --reload
```

El servidor queda disponible en: `http://127.0.0.1:8000`

La documentación interactiva (Swagger) en: `http://127.0.0.1:8000/docs`

---

## 4. Cómo autenticarse en Swagger

Todos los endpoints excepto `/api/auth/login` y `/api/auth/registro` requieren un token JWT.

**Pasos:**
1. Abrir `http://127.0.0.1:8000/docs`
2. Ir a `POST /api/auth/login` → **Try it out**
3. Llenar los campos:
   - `username`: `admin@hotel.com`
   - `password`: `admin123`
4. Hacer clic en **Execute**
5. Copiar el valor de `access_token` de la respuesta
6. Hacer clic en el botón **Authorize** (candado arriba a la derecha)
7. Pegar el token en el campo y hacer clic en **Authorize**

A partir de ese momento todas las peticiones llevan el token automáticamente.

**Usuarios de prueba disponibles:**

| Rol | Email | Contraseña |
|---|---|---|
| Administrador | `admin@hotel.com` | `admin123` |
| Huésped | `huesped@hotel.com` | `huesped123` |

---

## 5. Prueba completa del sistema

Seguir este orden para probar todos los módulos de forma encadenada.

---

### Módulo 1 — Autenticación

#### Registrar un usuario nuevo
`POST /api/auth/registro` — **No requiere token**
```json
{
  "email": "nuevo@hotel.com",
  "password": "123456"
}
```
> Devuelve un `access_token` directamente (el usuario queda logueado).  
> Si el email ya existe devuelve `409 Conflict`.  
> Si la contraseña tiene menos de 6 caracteres devuelve `422`.

#### Login
`POST /api/auth/login` — **No requiere token**

Llenar en el formulario:
- `username`: correo del usuario
- `password`: contraseña

> Devuelve `access_token` y `token_type`.

---

### Módulo 2 — Habitaciones

> Los endpoints de crear, cambiar estado y eliminar son exclusivos del **admin**.  
> Listar y obtener por id están disponibles para cualquier usuario logueado.

#### Crear habitación
`POST /api/habitaciones/` — **Solo admin**
```json
{
  "numero": "101",
  "tipo": "simple",
  "precio": 500,
  "disponible": true
}
```
> El campo `numero` es único. Si ya existe devuelve `409`.  
> Tipos sugeridos: `simple`, `doble`, `suite`, `familiar`.  
> `precio` se expresa en la moneda local (entero).

Crear varias habitaciones para tener datos suficientes:
```json
{ "numero": "102", "tipo": "doble", "precio": 800, "disponible": true }
{ "numero": "201", "tipo": "suite", "precio": 1500, "disponible": true }
{ "numero": "202", "tipo": "familiar", "precio": 1200, "disponible": true }
```

#### Listar habitaciones (con filtros opcionales)
`GET /api/habitaciones/` — **Cualquier usuario logueado**

Se pueden combinar los siguientes filtros en la URL:

| Parámetro | Tipo | Ejemplo | Descripción |
|---|---|---|---|
| `tipo` | string | `simple` | Filtra por tipo de habitación |
| `precio_min` | int | `500` | Precio mínimo |
| `precio_max` | int | `1000` | Precio máximo |
| `disponible` | bool | `true` | Solo disponibles o solo ocupadas |

Ejemplo en Swagger: dejar vacíos los filtros que no se necesiten.

#### Obtener una habitación por id
`GET /api/habitaciones/{id}` — **Cualquier usuario logueado**

Poner el `id` numérico de la habitación. Devuelve `404` si no existe.

#### Cambiar disponibilidad
`PATCH /api/habitaciones/{id}/estado?disponible=false` — **Solo admin**

El parámetro `disponible` va en la URL como query param (`true` o `false`).

#### Eliminar habitación
`DELETE /api/habitaciones/{id}` — **Solo admin**

Devuelve `204` sin cuerpo si se eliminó correctamente.

---

### Módulo 3 — Reservas

> Crear reserva y ver mis reservas: cualquier usuario logueado.  
> Listar todas, marcar como pagado: solo admin.

#### Crear reserva
`POST /api/reservas/` — **Cualquier usuario logueado**
```json
{
  "habitacion_id": 1,
  "fecha_checkin": "2026-07-10",
  "fecha_checkout": "2026-07-15"
}
```
> El `costo_total` se calcula automáticamente: `precio_habitacion × noches`.  
> Si la habitación no está disponible (`disponible: false`) devuelve `400`.  
> Si hay conflicto de fechas con otra reserva activa devuelve `400`.  
> Si `fecha_checkout` es igual o anterior a `fecha_checkin` devuelve `422`.  
> El estado inicial siempre es `"pendiente"`.

#### Ver mis reservas
`GET /api/reservas/mis-reservas` — **Cualquier usuario logueado**

Sin parámetros. Devuelve solo las reservas del usuario con el token activo.

#### Listar todas las reservas
`GET /api/reservas/` — **Solo admin**

Sin parámetros. Devuelve todas las reservas de todos los usuarios.

#### Marcar como pagado
`PATCH /api/reservas/{id}/pagar` — **Solo admin**

Poner el `id` de la reserva. Cambia el estado a `"pagado"` y genera automáticamente una factura.

#### Notificar pago pendiente
`POST /api/reservas/{id}/notificar-pago` — **Cualquier usuario logueado**

Simula el envío de una notificación al cliente. El resultado se imprime en los logs del servidor.

#### Cancelar reserva
`PATCH /api/reservas/{id}/cancelar` — **Cualquier usuario logueado**

Cambia el estado a `"cancelada"`.

---

### Módulo 4 — Facturas

> Las facturas se generan automáticamente al marcar una reserva como pagada.  
> No se crean manualmente.

#### Listar todas las facturas
`GET /api/facturas/` — **Solo admin**

Devuelve todas las facturas emitidas.

#### Obtener factura de una reserva
`GET /api/facturas/{reserva_id}` — **Cualquier usuario logueado**

Poner el `id` de la reserva (no de la factura). Devuelve `404` si la reserva aún no fue pagada.

---

### Módulo 5 — Dashboard

#### Ver estadísticas generales
`GET /api/dashboard/estadisticas` — **Solo admin**

Sin parámetros. Devuelve:
```json
{
  "reservas": {
    "total": 5,
    "pendientes": 2,
    "pagadas": 2,
    "canceladas": 1
  },
  "habitaciones": {
    "disponibles": 3,
    "ocupadas": 1
  },
  "ingresos_totales": 5000
}
```
> `ingresos_totales` suma el `costo_total` de todas las reservas con estado `"pagado"`.

---

### Módulo 6 — Usuarios

#### Ver mi perfil
`GET /api/usuarios/me` — **Cualquier usuario logueado**

Sin parámetros. Devuelve `id`, `email` y `role` del usuario autenticado.

#### Cambiar contraseña
`PATCH /api/usuarios/me/password` — **Cualquier usuario logueado**
```json
{
  "password_actual": "admin123",
  "password_nuevo": "nuevapass123"
}
```
> Si `password_actual` es incorrecto devuelve `400`.  
> `password_nuevo` debe tener al menos 6 caracteres.

#### Listar todos los usuarios
`GET /api/usuarios/` — **Solo admin**

Devuelve lista de todos los usuarios registrados con su `id`, `email` y `role`.

#### Eliminar usuario
`DELETE /api/usuarios/{id}` — **Solo admin**

El `id` es el UUID del usuario (visible en `GET /api/usuarios/`).  
> Devuelve `400` si intentas eliminar tu propia cuenta.  
> Devuelve `409` si el usuario tiene reservas asociadas.

---

## 6. Flujo de prueba recomendado

Para probar el sistema completo de inicio a fin:

1. Login como **admin**
2. Crear 3 o 4 habitaciones con tipos y precios distintos
3. Listar habitaciones con filtros para verificar que funcionan
4. Registrar un usuario nuevo (`POST /api/auth/registro`)
5. Login con el usuario nuevo
6. Crear una reserva con fechas futuras
7. Intentar crear otra reserva con fechas solapadas en la misma habitación → debe dar `400`
8. Ver mis reservas con el usuario nuevo
9. Login como **admin**
10. Listar todas las reservas
11. Marcar la reserva como pagada → se genera la factura automáticamente
12. Consultar la factura generada (`GET /api/facturas/{reserva_id}`)
13. Ver el dashboard para verificar que los ingresos se actualizaron
14. Cancelar una segunda reserva y verificar que el dashboard lo refleja
15. Listar usuarios y probar eliminar el usuario de prueba

---

## 7. Códigos de respuesta comunes

| Código | Significado |
|---|---|
| `200` | OK — operación exitosa |
| `201` | Created — recurso creado correctamente |
| `204` | No Content — eliminado correctamente |
| `400` | Bad Request — datos inválidos o regla de negocio violada |
| `401` | Unauthorized — token ausente o expirado |
| `403` | Forbidden — no tienes permisos para esta acción |
| `404` | Not Found — el recurso no existe |
| `409` | Conflict — duplicado o restricción de integridad |
| `422` | Unprocessable Entity — error de validación en los campos enviados |
