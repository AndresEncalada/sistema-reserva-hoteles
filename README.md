# API Sistema de Reservas de Hotel

Este repositorio contiene el backend de un sistema de reservas de hotel, desarrollado con el framework FastAPI en Python. El sistema expone una interfaz de programación de aplicaciones (API) RESTful diseñada para gestionar operaciones de hospedaje, facturación y administración, integrando seguridad mediante JSON Web Tokens (JWT) y Control de Acceso Basado en Roles (RBAC).

## 1. Arquitectura y Tecnologías

El proyecto implementa una arquitectura basada en capas siguiendo el patrón **MRSC** (Modelos, Repositorios, Servicios y Controladores), lo cual garantiza una clara separación de responsabilidades y facilita la mantenibilidad del código.

* **Framework Web:** FastAPI (con validación de datos a través de Pydantic).
* **Gestor de Paquetes y Entorno:** uv (para resolución rápida de dependencias orientada a Python 3.12+).
* **Base de Datos:** PostgreSQL 15 (desplegado mediante Docker).
* **ORM:** SQLAlchemy 2.0 en modo asíncrono, operando con el driver asyncpg.
* **Seguridad y Autenticación:** Implementación nativa de JWT (pyjwt) y hashing de contraseñas mediante bcrypt (sin passlib).
* **Gestión de Configuración:** pydantic-settings para el manejo de variables de entorno.

### Módulos Principales
La API está segmentada en los siguientes módulos funcionales:
* **Autenticación:** Generación y validación de tokens JWT.
* **Usuarios:** Gestión de perfiles y credenciales de acceso.
* **Habitaciones:** Catálogo y disponibilidad de habitaciones.
* **Reservas:** Ciclo de vida de las reservas (creación, confirmación, cancelación).
* **Facturas:** Registro financiero asociado a las reservas.
* **Dashboard:** Indicadores y métricas agregadas para la administración.

## 2. Estructura de Directorios

La estructura del código fuente está organizada dentro del directorio app/ para aislar la lógica de la aplicación de la configuración del entorno y las dependencias:

```text
sistema-reserva-hoteles/
├── app/
│   ├── controllers/      # Controladores que definen las rutas y endpoints de la API (FastAPI Routers)
│   ├── core/             # Configuraciones globales (Conexión a BD, manejo de JWT y settings)
│   ├── models/           # Definición de tablas ORM (SQLAlchemy) y esquemas de validación (Pydantic)
│   ├── repositories/     # Capa de acceso a datos (Transacciones directas con la base de datos)
│   ├── scripts/          # Scripts de inicialización y población de datos de prueba (Seeders)
│   ├── services/         # Lógica de negocio que orquesta la comunicación entre repositorios y controladores
│   └── main.py           # Punto de entrada de la aplicación y registro de rutas
├── docs/                 # Recursos gráficos y documentación adicional
├── .env.example          # Plantilla con las variables de entorno requeridas
├── docker-compose.yml    # Definición de servicios para infraestructura local (Base de datos PostgreSQL)
├── pyproject.toml        # Declaración de metadatos del proyecto y dependencias de Python
└── README.md             # Documentación principal del proyecto
```
## 3. Configuración del Entorno de Desarrollo

El siguiente procedimiento describe los pasos necesarios para desplegar el entorno local de desarrollo. Se requiere tener instalados uv y docker (con docker compose).

**1. Configuración de Variables de Entorno**
Crear una copia del archivo de configuración para adaptar las credenciales locales:
cp .env.example .env

**2. Instalación de Dependencias**
Sincronizar el entorno virtual de Python utilizando el gestor de paquetes uv:
uv sync

**3. Despliegue de Infraestructura Local**
Levantar el contenedor de PostgreSQL en segundo plano:
docker compose up -d

**4. Inicialización de la Base de Datos**
Crear las estructuras de tablas requeridas por los modelos de SQLAlchemy:
uv run app/scripts/init_db.py

**5. Población de Datos Iniciales (Seeding)**
Cargar los usuarios base y, opcionalmente, la información de demostración:
uv run app/scripts/seed_users.py
uv run app/scripts/seed_demo_data.py

**6. Ejecución del Servidor Web**
Iniciar el servidor de desarrollo uvicorn con recarga automática activada:
uv run uvicorn main:app --app-dir app --reload

## 4. Control de Acceso y Autorización

La API restringe el acceso a sus recursos de acuerdo con el rol del usuario autenticado. El flujo de autenticación opera de la siguiente manera:

1. El cliente envía sus credenciales al endpoint de login.
2. El servidor verifica los datos y retorna un token JWT firmado.
3. El cliente incluye dicho token en el encabezado Authorization: Bearer <token> para subsecuentes peticiones.

**Roles y Permisos:**
* **Rol de Usuario (user):** Acceso permitido a endpoints generales (creación de reservas propias, consultas de perfil).
* **Rol de Administrador (admin):** Acceso total a las métricas del sistema, facturación general y alteración de disponibilidad de habitaciones (controlado internamente mediante inyección de dependencias require_role(Role.ADMIN)).

*Credenciales generadas por el script seed_users.py:*
* Administrador: admin@hotel.com / admin123
* Huésped: huesped@hotel.com / huesped123

## 5. Documentación de la API

FastAPI genera automáticamente la especificación OpenAPI del proyecto. Una vez en ejecución, la documentación interactiva y los esquemas pueden ser consultados en las siguientes rutas:

* **Swagger UI:** http://127.0.0.1:8000/docs (Permite la ejecución directa de pruebas HTTP y autorización).
* **ReDoc:** http://127.0.0.1:8000/redoc (Vista de documentación estructurada y detallada).
* **Esquema JSON:** http://127.0.0.1:8000/openapi.json
