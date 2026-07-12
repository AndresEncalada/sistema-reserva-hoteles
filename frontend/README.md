# Sistema de Reserva de Hoteles - Frontend

Frontend desarrollado con React + TypeScript + Vite + Tailwind CSS para el sistema de reserva de hoteles.

## Tecnologías

- **React 18** con TypeScript
- **Vite** - Build tool rápido
- **Tailwind CSS** - Framework de estilos
- **React Router** - Enrutamiento
- **Axios** - Cliente HTTP
- **Lucide React** - Íconos

## Instalación

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Construir para producción
npm run build
```
## Estructura del proyecto
```bash
src/
├── components/      # Componentes reutilizables
│   ├── layout/     # Layout (Navbar, Footer)
│   └── ui/         # Componentes UI (Button, Input, Card)
├── pages/          # Páginas de la aplicación
│   ├── auth/       # Login, Registro
│   └── dashboard/  # Dashboards de usuario/admin
├── services/       # Llamadas a la API
├── hooks/          # Custom hooks
├── types/          # Tipos TypeScript
└── utils/          # Funciones auxiliares
```

## Backend
!!! info Este frontend consume la API del backend desarrollado en FastAPI. Ver repositorio principal para más detalles.