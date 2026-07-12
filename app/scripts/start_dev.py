#!/usr/bin/env python3
"""
Script para iniciar el sistema completo (Docker + Backend + Frontend)
Uso: uv run start-dev
"""

import subprocess
import sys
import time
import os
from pathlib import Path
import signal

def get_project_root():
    """Obtener la raíz del proyecto"""
    return Path(__file__).parent.parent.parent

def check_env_file(root: Path):
    """Verificar y crear archivo .env si no existe"""
    env_file = root / ".env"
    env_example = root / ".env.example"
    
    if not env_file.exists():
        if env_example.exists():
            print("\nArchivo .env no encontrado, creando desde .env.example...")
            import shutil
            shutil.copy(env_example, env_file)
            print("Archivo .env creado correctamente")
            print("IMPORTANTE: Revisa las variables en .env y ajústalas si es necesario")
            time.sleep(2)
        else:
            print("ERROR: No se encontró .env.example")
            print("Crea el archivo .env manualmente con las variables requeridas")
            sys.exit(1)

def check_docker_available():
    """Verificar si Docker está disponible"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            shell=(os.name == 'nt')
        )
        return result.returncode == 0
    except Exception:
        return False

def check_docker_compose_running(root: Path):
    """Verificar si los contenedores ya están corriendo"""
    try:
        result = subprocess.run(
            ["docker", "compose", "ps", "--format", "json"],
            cwd=root,
            capture_output=True,
            text=True,
            shell=(os.name == 'nt')
        )
        if result.returncode == 0 and result.stdout.strip():
            return "running" in result.stdout.lower()
        return False
    except Exception:
        return False

def start_docker(root: Path):
    """Iniciar servicios de Docker (PostgreSQL)"""
    print("\n" + "="*60)
    print("Iniciando servicios Docker (PostgreSQL)...")
    print("="*60 + "\n")
    
    if os.name == 'nt':
        process = subprocess.Popen(
            "docker compose up -d",
            cwd=root,
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        process = subprocess.Popen(
            ["docker", "compose", "up", "-d"],
            cwd=root
        )
    
    process.wait()
    
    if process.returncode != 0:
        print("ERROR: No se pudieron iniciar los servicios Docker")
        print("Verifica que Docker Desktop esté corriendo")
        sys.exit(1)
    
    print("Servicios Docker iniciados correctamente")
    print("Esperando a que PostgreSQL esté listo...")
    time.sleep(5)

def start_backend(root: Path):
    """Iniciar el backend FastAPI"""
    print("\n" + "="*60)
    print("Iniciando Backend (FastAPI)...")
    print("="*60 + "\n")
    
    if os.name == 'nt':
        process = subprocess.Popen(
            "uv run uvicorn main:app --app-dir app --reload --host 0.0.0.0 --port 8000",
            cwd=root,
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        process = subprocess.Popen(
            ["uv", "run", "uvicorn", "main:app", "--app-dir", "app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            cwd=root
        )
    return process

def start_frontend(root: Path):
    """Iniciar el frontend React"""
    print("\n" + "="*60)
    print("Iniciando Frontend (React)...")
    print("="*60 + "\n")
    
    frontend_dir = root / "frontend"
    
    if os.name == 'nt':
        process = subprocess.Popen(
            "npm run dev",
            cwd=frontend_dir,
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir
        )
    return process

def check_backend_ready():
    """Verificar si el backend está listo"""
    import urllib.request
    import urllib.error
    
    for i in range(10):
        try:
            urllib.request.urlopen("http://localhost:8000/docs", timeout=2)
            return True
        except:
            time.sleep(1)
    return False

def print_startup_info():
    """Mostrar información de inicio"""
    print("\n" + "="*60)
    print("SISTEMA DE RESERVA DE HOTELES - INICIADO")
    print("="*60)
    print("\nServicios disponibles:")
    print("  - Backend API:  http://localhost:8000")
    print("  - Frontend:     http://localhost:5173")
    print("  - API Docs:     http://localhost:8000/docs")
    print("  - PostgreSQL:   localhost:5432")
    print("\nPresiona Ctrl+C para detener todos los servicios")
    print("="*60 + "\n")

def cleanup(backend_proc, frontend_proc):
    """Limpiar procesos al salir"""
    print("\n\nDeteniendo servicios...")
    
    if backend_proc:
        try:
            if os.name == 'nt':
                backend_proc.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                backend_proc.terminate()
            backend_proc.wait(timeout=5)
            print("Backend detenido")
        except Exception as e:
            print(f"Error al detener backend: {e}")
    
    if frontend_proc:
        try:
            if os.name == 'nt':
                frontend_proc.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                frontend_proc.terminate()
            frontend_proc.wait(timeout=5)
            print("Frontend detenido")
        except Exception as e:
            print(f"Error al detener frontend: {e}")
    
    print("\nSistema cerrado correctamente\n")

def main():
    """Función principal"""
    root = get_project_root()
    
    # Verificar que estamos en la raíz del proyecto
    if not (root / "pyproject.toml").exists():
        print("ERROR: No se encontró pyproject.toml")
        print("Asegúrate de ejecutar este script desde la raíz del proyecto")
        sys.exit(1)
    
    # Verificar que existe el frontend
    if not (root / "frontend" / "package.json").exists():
        print("ERROR: No se encontró el directorio frontend/")
        print("Asegúrate de que el frontend está instalado")
        sys.exit(1)
    
    # Verificar y crear .env
    check_env_file(root)
    
    # Verificar Docker
    if not check_docker_available():
        print("ERROR: Docker no está disponible")
        print("Instala Docker Desktop y asegúrate de que esté corriendo")
        sys.exit(1)
    
    # Iniciar Docker si no está corriendo
    if not check_docker_compose_running(root):
        start_docker(root)
    else:
        print("\nServicios Docker ya están corriendo")
    
    backend_proc = None
    frontend_proc = None
    
    try:
        # Iniciar backend
        backend_proc = start_backend(root)
        
        # Esperar a que el backend esté listo
        print("\nVerificando que el backend esté listo...")
        if not check_backend_ready():
            print("ERROR: El backend no respondió después de 10 segundos")
            print("Revisa los logs del backend para más detalles")
            if backend_proc.poll() is not None:
                print("El proceso del backend terminó con error")
            cleanup(backend_proc, None)
            sys.exit(1)
        
        print("Backend listo")
        time.sleep(1)
        
        # Iniciar frontend
        frontend_proc = start_frontend(root)
        time.sleep(2)
        
        # Mostrar información
        print_startup_info()
        
        # Mantener el script corriendo
        while True:
            if backend_proc.poll() is not None:
                print("ADVERTENCIA: Backend se ha detenido inesperadamente")
                break
            if frontend_proc.poll() is not None:
                print("ADVERTENCIA: Frontend se ha detenido inesperadamente")
                break
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        cleanup(backend_proc, frontend_proc)

if __name__ == "__main__":
    main()