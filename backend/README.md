# Backend

Contenedor base con Python 3.12, FastAPI y Uvicorn.

El backend se ejecuta mediante Docker Compose desde la raíz del proyecto.

```powershell
docker compose up -d --build backend
docker compose logs -f backend
```

Endpoints iniciales:

- `GET /health`
- Documentación Swagger: `http://localhost:8001/docs`
- Salud: `http://localhost:8001/health`
