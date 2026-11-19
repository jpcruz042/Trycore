# Trycore EVM Project

Aplicación fullstack para administrar proyectos, actividades e indicadores de Valor Ganado.

## Stack planeado

- PostgreSQL 16
- Python / FastAPI
- Angular
- Docker Compose

## Requisitos

- Docker Desktop
- Docker Compose
- Git

## Iniciar la base de datos

```powershell
Copy-Item .env.example .env
docker compose up -d postgres
```

Verificar el estado:

```powershell
docker compose ps
docker compose exec postgres pg_isready -U trycore -d trycore
```

Inspeccionar el esquema:

```powershell
docker compose exec postgres psql -U trycore -d trycore -c "\dt"
```

La base quedará disponible en `localhost:5433` para evitar conflictos con otros contenedores PostgreSQL.

## Ejecutar el backend

```powershell
docker compose up -d --build backend
```

- API: `http://localhost:8001`
- Salud: `http://localhost:8001/health`
- Swagger: `http://localhost:8001/docs`

## Detener el entorno

```powershell
docker compose stop
```

Eliminar contenedor y datos persistidos:

```powershell
docker compose down -v
```

## Próximos pasos

1. Implementar los modelos y endpoints FastAPI.
2. Implementar el frontend Angular.
3. Completar las pruebas unitarias e integración.
4. Documentar las decisiones de IA y EVM en `AI_PROCESS.md`.
