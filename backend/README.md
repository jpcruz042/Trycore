# Backend

Contenedor base con Python 3.12, FastAPI y Uvicorn.

El backend se ejecuta mediante Docker Compose desde la raíz del proyecto.

```powershell
docker compose up -d --build backend
docker compose logs -f backend
```

Endpoints:

- `GET /health`
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

URLs locales:

- API: `http://localhost:8001`
- Salud: `http://localhost:8001/health`
- Swagger: `http://localhost:8001/docs`

Pruebas:

```powershell
docker compose exec backend python -m pytest tests -v --cov=app --cov-report=term-missing
```
