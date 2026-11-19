# Trycore EVM Project

Aplicación fullstack para administrar proyectos, actividades e indicadores Earned Value Management (EVM).

## Entregables incluidos

- Aplicación Dockerizada con PostgreSQL, FastAPI y Angular.
- Base de datos reproducible con datos de demostración.
- API documentada con OpenAPI/Swagger.
- Pruebas unitarias de EVM e integración HTTP.
- Documento `AI_PROCESS.md` con el registro del proceso de desarrollo.

## Tecnologías

- PostgreSQL 16.
- Python 3.12 y FastAPI.
- SQLAlchemy y asyncpg.
- Angular 20.
- Docker Compose y Nginx.

## Requisitos previos

- Docker Desktop iniciado.
- Docker Compose.
- Navegador web moderno.
- PowerShell 5.1 o posterior.

No se requiere instalar Python ni Node.js directamente: las aplicaciones se ejecutan dentro de Docker.

## Puertos utilizados

- Frontend Angular: `http://localhost:4200`
- Backend FastAPI: `http://localhost:8001`
- Swagger: `http://localhost:8001/docs`
- Salud del backend: `http://localhost:8001/health`
- PostgreSQL: `localhost:5433`

Los puertos 5433 y 8001 se seleccionaron para evitar conflictos con PostgreSQL y aplicaciones locales existentes.

## Inicio rápido

Desde la carpeta raíz del proyecto:

```powershell
Copy-Item .env.example .env
docker compose down -v
docker compose up -d --build
```

Espere a que los contenedores estén saludables:

```powershell
docker compose ps
```

Abrir:

- `http://localhost:4200`
- `http://localhost:8001/docs`

El comando `docker compose down -v` elimina los datos anteriores y permite que los scripts de inicialización creen nuevamente el proyecto de demostración.

## Datos de demostración

La primera inicialización crea automáticamente:

- Proyecto: `Proyecto Demo Trycore`.
- Actividad: `Diseño`.
- Actividad: `Desarrollo`.
- Actividad: `Pruebas`.

Esto permite demostrar inmediatamente el tablero EVM sin cargar datos manualmente.

## Comandos útiles

Verificar salud de PostgreSQL:

```powershell
docker compose exec postgres pg_isready -U trycore -d trycore
```

Consultar tablas:

```powershell
docker compose exec postgres psql -U trycore -d trycore -c "\dt"
```

Ver registros del backend:

```powershell
docker compose logs -f backend
```

Detener todos los servicios conservando los datos:

```powershell
docker compose stop
```

Reiniciar servicios:

```powershell
docker compose start
```

Eliminar contenedores y datos persistidos:

```powershell
docker compose down -v
```

## Endpoints principales

- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}`
- `PUT /projects/{project_id}`
- `DELETE /projects/{project_id}`
- `GET /projects/{project_id}/evm`
- `POST /projects/{project_id}/activities`
- `GET /projects/{project_id}/activities`
- `GET /projects/{project_id}/activities/{activity_id}`
- `PUT /projects/{project_id}/activities/{activity_id}`
- `DELETE /projects/{project_id}/activities/{activity_id}`

## Pruebas

Ejecutar toda la suite dentro del contenedor:

```powershell
docker compose exec backend python -m pytest tests -v
```

Medir cobertura de la lógica EVM:

```powershell
docker compose exec backend python -m pytest tests -v --cov=app.evm --cov-report=term-missing
```

## Indicadores EVM

- PV = Porcentaje planificado × BAC.
- EV = Porcentaje real × BAC.
- CV = EV − AC.
- SV = EV − PV.
- CPI = EV / AC.
- SPI = EV / PV.
- EAC = BAC / CPI.
- VAC = BAC − EAC.

CPI mayor que 1 indica eficiencia de costo. CPI menor que 1 indica sobre presupuesto. SPI mayor que 1 indica trabajo adelantado. SPI menor que 1 indica atraso.

El sistema retorna `not_available` o un valor nulo cuando no existe denominador válido, por ejemplo AC igual a cero o PV igual a cero.

## Configuración local opcional

El archivo `.env.example` puede copiarse como `.env`:

```powershell
Copy-Item .env.example .env
```

Las credenciales contenidas son únicamente para desarrollo local. Cambie `POSTGRES_PASSWORD` antes de utilizar este proyecto en un entorno compartido.

## Generar el paquete comprimido

Desde la carpeta raíz:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package-project.ps1
```

El paquete `Trycore-EVM-Entrega.zip` se crea junto a la carpeta raíz. El archivo excluye `.git`, `.env`, dependencias locales, compilados y directorios temporales.

## Detalles del repositorio entregado

- `database/init/`: scripts de creación y datos de demostración.
- `backend/`: API FastAPI, modelos, esquemas y pruebas.
- `frontend/`: aplicación Angular y configuración Docker/Nginx.
- `AI_PROCESS.md`: documentación del uso de inteligencia artificial.
- `docker-compose.yml`: orquestación completa del entorno.
