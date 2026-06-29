# Informe técnico: Sistema de Reserva de Hoteles

**Grupo:** Grupo 1

**Integrantes:**

- Andrés Encalada
- Nayeli Barbecho
- Jordy Romero
- David Villa
- Karen Ortiz

**Proyecto:** API REST para la gestión de reservas de hotel

**Repositorio:** `https://github.com/AndresEncalada/sistema-reserva-hoteles`

## 1. Resumen

El presente informe describe el desarrollo de una API REST para un sistema de reserva de hoteles. La aplicación permite registrar e iniciar sesión de usuarios, administrar habitaciones, crear reservas, marcar pagos, generar facturas y consultar estadísticas administrativas.

La solución fue desarrollada con FastAPI, SQLAlchemy asíncrono y PostgreSQL. Además, cumple con el requisito de publicar los servicios con documentación mediante Swagger, disponible en la ruta `/docs`.

## 2. Objetivo

El objetivo del proyecto es implementar un backend funcional para la gestión de reservas hoteleras, aplicando una arquitectura organizada por capas, autenticación mediante JWT, control de acceso por roles y documentación interactiva de los endpoints mediante Swagger UI.

## 3. Tecnologías utilizadas

| Tecnología | Uso |
| --- | --- |
| Python 3.12+ | Lenguaje principal del backend |
| FastAPI | Framework web para exponer la API REST |
| SQLAlchemy 2.0 async | ORM y acceso asíncrono a la base de datos |
| asyncpg | Driver asíncrono para PostgreSQL |
| PostgreSQL 15 | Base de datos relacional |
| Docker Compose | Levantamiento local de la base de datos |
| Pydantic | Validación de datos y esquemas de entrada/salida |
| JWT | Autenticación sin estado mediante tokens |
| bcrypt | Hash seguro de contraseñas |
| uv | Gestión de dependencias y entorno de ejecución |

## 4. Inicialización del proyecto

### 4.1. Requisitos

- Python 3.12 o superior.
- Docker y Docker Compose.
- `uv` instalado.

### 4.2. Variables de entorno

Para ejecutar el sistema se debe crear un archivo `.env` en la raíz del proyecto, tomando como base el archivo `.env.example`:

```env
SECRET_KEY=clave-secreta-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql+asyncpg://hotel_user:hotel_password@localhost:5432/hotel_reservations
```

### 4.3. Comandos de arranque

Los siguientes comandos permiten instalar dependencias, levantar la base de datos, crear las tablas, cargar datos de prueba e iniciar el servidor:

```bash
uv sync
docker compose up -d
uv run app/scripts/init_db.py
uv run app/scripts/seed_users.py
uv run app/scripts/seed_demo_data.py
uv run uvicorn main:app --app-dir app --reload
```

Cuando el servidor esté iniciado, la API queda disponible en:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

### 4.4. Credenciales de prueba

| Rol | Email | Password |
| --- | --- | --- |
| Administrador | `admin@hotel.com` | `admin123` |
| Huésped | `huesped@hotel.com` | `huesped123` |
| Administrador demo | `recepcion@hotel.com` | `recepcion123` |
| Huésped demo | `maria.gomez@hotel.com` | `maria123` |
| Huésped demo | `carlos.perez@hotel.com` | `carlos123` |
| Huésped demo | `ana.torres@hotel.com` | `ana123` |

### 4.5. Datos demo adicionales

Se agregó el script `app/scripts/seed_demo_data.py` para cargar información de prueba más completa. El script es idempotente, por lo que puede ejecutarse varias veces sin duplicar los mismos registros demo.

El script crea o actualiza:

- 4 usuarios demo adicionales.
- 8 habitaciones de tipo `Individual`, `Doble`, `Suite` y `Familiar`.
- 6 reservas en estados `pagado`, `pendiente` y `cancelada`.
- 3 facturas asociadas a reservas pagadas.

Después de ejecutar `seed_users.py` y `seed_demo_data.py`, la base queda con:

| Entidad | Cantidad |
| --- | ---: |
| Usuarios | 6 |
| Habitaciones | 8 |
| Reservas | 6 |
| Facturas | 3 |

## 5. Documentación Swagger

FastAPI genera automáticamente la especificación OpenAPI a partir de:

- Rutas declaradas con `APIRouter`.
- Modelos Pydantic usados como request y response models.
- Tags configurados en los controladores.
- Dependencia OAuth2 Bearer usada para endpoints protegidos.

Para probar los servicios protegidos en Swagger se realiza el siguiente procedimiento:

1. Abrir `http://127.0.0.1:8000/docs`.
2. Ejecutar `POST /api/auth/login`.
3. Ingresar el email en el campo `username` y la contraseña en `password`.
4. Copiar el `access_token`.
5. Presionar `Authorize`.
6. Pegar el token como Bearer token.

### 5.1. Evidencia visual de Swagger

Las siguientes capturas muestran que los servicios fueron publicados y probados mediante Swagger UI.

#### Vista general de Swagger

<p align="center">
  <img src="docs/img/swagger-general.png" alt="Vista general de Swagger" width="70%">
</p>

En esta vista se observan los módulos documentados por tags: Autenticación, Usuarios, Habitaciones, Reservas, Facturas y Dashboard. Cada sección agrupa sus endpoints, métodos HTTP, parámetros y esquemas de respuesta.

#### Autorización con JWT

<p align="center">
  <img src="docs/img/swagger-authorize.png" alt="Autorización JWT en Swagger" width="65%">
</p>

La ventana de autorización permite registrar el token JWT devuelto por `POST /api/auth/login`. Con esto Swagger envía el token Bearer en las peticiones protegidas.

#### Endpoint administrativo de estadísticas

<p align="center">
  <img src="docs/img/estadisticas.png" alt="Endpoint de estadísticas en Swagger" width="70%">
</p>

La captura evidencia el consumo de `/api/dashboard/estadisticas`, endpoint protegido para administradores. Este servicio devuelve totales de reservas, habitaciones disponibles/ocupadas e ingresos calculados desde la base de datos.

## 6. Estructura del proyecto

```text
.
├── app
│   ├── controllers      # Endpoints HTTP y dependencias de FastAPI
│   ├── core             # Configuración, seguridad y conexión a base de datos
│   ├── models           # Modelos SQLAlchemy y esquemas Pydantic
│   ├── repositories     # Consultas y persistencia de datos
│   ├── scripts          # Inicialización y datos de prueba
│   ├── services         # Reglas de negocio
│   └── main.py          # Punto de entrada de FastAPI
├── docs
│   └── img              # Capturas de Swagger para evidencias del informe
├── docker-compose.yml   # Servicio PostgreSQL
├── pyproject.toml       # Dependencias del proyecto
├── README.md            # Guía rápida
└── INFORME.md           # Informe técnico del sistema
```

## 7. Arquitectura

El sistema sigue una arquitectura por capas similar a Modelo-Repositorio-Servicio-Controlador.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontSize": "12px"}, "flowchart": {"nodeSpacing": 25, "rankSpacing": 25}}}%%
flowchart TD
    Client[Cliente / Swagger] --> API[FastAPI]
    API --> Controllers[Controllers]
    Controllers --> Services[Services]
    Services --> Repos[Repositories]
    Repos --> DB[(PostgreSQL)]
    Controllers --> Schemas[Pydantic]
    Repos --> Models[SQLAlchemy]
    API --> Security[JWT / Roles]
```

Responsabilidades principales:

- `controllers`: reciben la petición HTTP, validan dependencias y devuelven respuestas.
- `services`: concentran reglas de negocio, como pagos, cancelaciones y cálculos.
- `repositories`: encapsulan consultas SQLAlchemy.
- `models`: definen tablas de base de datos y esquemas de entrada/salida.
- `core`: contiene configuración, seguridad y sesión de base de datos.

## 8. Módulos implementados

### 8.1. Autenticación

Permite registrar usuarios e iniciar sesión. El login retorna un JWT con el email y rol del usuario.

Endpoints:

| Método | Ruta | Acceso | Descripción |
| --- | --- | --- | --- |
| POST | `/api/auth/login` | Público | Autentica usuario y devuelve token |
| POST | `/api/auth/registro` | Público | Registra un usuario nuevo |

### 8.2. Usuarios

Permite consultar el perfil autenticado, cambiar contraseña y administrar usuarios desde el rol administrador.

| Método | Ruta | Acceso | Descripción |
| --- | --- | --- | --- |
| GET | `/api/usuarios/me` | Usuario autenticado | Obtiene perfil propio |
| PATCH | `/api/usuarios/me/password` | Usuario autenticado | Cambia contraseña |
| GET | `/api/usuarios/` | Admin | Lista usuarios |
| DELETE | `/api/usuarios/{id}` | Admin | Elimina usuario |

### 8.3. Habitaciones

Permite consultar habitaciones y administrarlas desde el rol administrador.

| Método | Ruta | Acceso | Descripción |
| --- | --- | --- | --- |
| GET | `/api/habitaciones/` | Usuario autenticado | Lista habitaciones con filtros |
| GET | `/api/habitaciones/{id}` | Usuario autenticado | Obtiene habitación por id |
| POST | `/api/habitaciones/` | Admin | Crea habitación |
| PATCH | `/api/habitaciones/{id}/estado` | Admin | Cambia disponibilidad |
| DELETE | `/api/habitaciones/{id}` | Admin | Elimina habitación |

### 8.4. Reservas

Permite crear reservas, consultar reservas propias, administrar pagos y cancelar reservas.

| Método | Ruta | Acceso | Descripción |
| --- | --- | --- | --- |
| POST | `/api/reservas/` | Usuario autenticado | Crea reserva |
| GET | `/api/reservas/` | Admin | Lista todas las reservas |
| GET | `/api/reservas/mis-reservas` | Usuario autenticado | Lista reservas propias |
| PATCH | `/api/reservas/{id}/pagar` | Admin | Marca una reserva como pagada y genera factura |
| POST | `/api/reservas/{id}/notificar-pago` | Usuario autenticado | Simula notificación de pago pendiente |
| PATCH | `/api/reservas/{id}/cancelar` | Usuario autenticado | Cancela reserva |

### 8.5. Facturas

Permite consultar facturas generadas por reservas pagadas.

| Método | Ruta | Acceso | Descripción |
| --- | --- | --- | --- |
| GET | `/api/facturas/` | Admin | Lista todas las facturas |
| GET | `/api/facturas/{reserva_id}` | Usuario autenticado | Obtiene factura por reserva |

### 8.6. Dashboard

Módulo administrativo para consultar indicadores generales.

| Método | Ruta | Acceso | Descripción |
| --- | --- | --- | --- |
| GET | `/api/dashboard/estadisticas` | Admin | Muestra estadísticas de reservas, habitaciones e ingresos |

## 9. Seguridad

La seguridad se basa en JWT y control de acceso por roles.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontSize": "11px", "actorBkg": "#f8fafc"}}}%%
sequenceDiagram
    actor Usuario
    participant API
    participant Auth
    participant DB as PostgreSQL

    Usuario->>API: Login
    API->>Auth: Credenciales
    Auth->>DB: Buscar usuario
    DB-->>Auth: Usuario y rol
    Auth-->>API: JWT
    API-->>Usuario: Token
    Usuario->>API: Petición protegida
    API->>API: Validar JWT / rol
    API-->>Usuario: Respuesta
```

Reglas aplicadas:

- Endpoints públicos: login y registro.
- Endpoints autenticados: perfil, habitaciones, reservas propias, factura por reserva.
- Endpoints administrativos: administración de habitaciones, usuarios, reservas, facturas y dashboard.

## 10. Modelo de datos

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontSize": "11px"}}}%%
erDiagram
    USERS ||--o{ RESERVAS : realiza
    HABITACIONES ||--o{ RESERVAS : asignada_en
    RESERVAS ||--o| FACTURAS : genera
    USERS ||--o{ FACTURAS : recibe

    USERS {
        uuid id PK
        string email UK
        string hashed_password
        enum role
    }

    HABITACIONES {
        int id PK
        string numero UK
        string tipo
        int precio
        bool disponible
    }

    RESERVAS {
        int id PK
        uuid usuario_id FK
        int habitacion_id FK
        string estado
        date fecha_checkin
        date fecha_checkout
        int costo_total
    }

    FACTURAS {
        int id PK
        int reserva_id FK
        uuid usuario_id FK
        int monto
        date fecha_emision
    }
```

## 11. Flujo principal de reserva

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontSize": "12px"}, "flowchart": {"nodeSpacing": 25, "rankSpacing": 25}}}%%
flowchart TD
    A[Usuario] --> B[Consulta habitaciones]
    B --> C[Elige fechas]
    C --> D[Crear reserva]
    D --> E{Disponible}
    E -- No --> F[Error 400]
    E -- Si --> G[Reserva pendiente]
    G --> H[Admin confirma pago]
    H --> I[Reserva pagada]
    I --> J[Factura]
```

## 12. Reglas de negocio relevantes

- La fecha de salida debe ser posterior a la fecha de ingreso.
- Solo usuarios autenticados pueden consultar habitaciones y crear reservas.
- Solo administradores pueden crear, eliminar o cambiar disponibilidad de habitaciones.
- Solo administradores pueden listar todas las reservas y marcar pagos.
- Al marcar una reserva como pagada, se genera una factura si todavía no existe.
- El dashboard calcula totales de reservas, estados, habitaciones disponibles/ocupadas e ingresos.

## 13. Scripts de soporte

| Script | Descripción |
| --- | --- |
| `app/scripts/init_db.py` | Crea las tablas declaradas con SQLAlchemy en PostgreSQL |
| `app/scripts/seed_users.py` | Crea usuarios básicos de prueba: admin y huésped |
| `app/scripts/seed_demo_data.py` | Carga datos demo completos: usuarios, habitaciones, reservas y facturas |

## 14. Endpoints de soporte y documentación

| Ruta | Descripción |
| --- | --- |
| `/` | Mensaje de bienvenida |
| `/docs` | Swagger UI |
| `/redoc` | Documentación ReDoc |
| `/openapi.json` | Especificación OpenAPI |

## 15. Conclusiones

El proyecto cumple con la publicación de servicios documentados mediante Swagger. La API está organizada por módulos, utiliza validación con Pydantic y separa responsabilidades en capas, lo cual facilita el mantenimiento, la comprensión del código y la posible incorporación de nuevas funcionalidades.

Además, se implementó autenticación con JWT y control de acceso por roles, permitiendo diferenciar operaciones públicas, operaciones de usuarios autenticados y operaciones exclusivas para administradores. También se prepararon datos de prueba para demostrar el funcionamiento de los módulos principales desde Swagger.

Posibles mejoras futuras:

- Agregar migraciones con Alembic.
- Agregar pruebas automatizadas.
- Restringir que un usuario solo pueda cancelar reservas propias.
- Registrar notificaciones reales por correo o mensajeria.
- Agregar paginacion en listados administrativos.
